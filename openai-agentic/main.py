import asyncio
import json
import os
import sys
import argparse
import logging
from datetime import datetime, UTC

# Ensure project root is on path so backend/ imports work (same pattern as LLMs/main.py)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, '.env'))

from services.generator_agent_service import GeneratorAgentService
from services.detector_agent_service import DetectorAgentService
from utils.db_utils import init_db, create_round, update_round, save_email, save_log


def parse_args():
    parser = argparse.ArgumentParser(description="OpenAI Agents SDK - Phishing email generation & detection")
    parser.add_argument("--rounds", type=int, help="Number of rounds to run")
    parser.add_argument("--emails-per-round", type=int, dest="emails_per_round", help="Number of emails per round")
    return parser.parse_args()


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("openai_agentic")
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    fh = logging.FileHandler("openai_agentic.log", mode='a')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(fmt)
    ch.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger


def prompt_int(message: str, default: int = 1) -> int:
    try:
        value = int(input(message).strip() or default)
        return value if value > 0 else default
    except ValueError:
        print(f"Invalid input. Using default value of {default}.")
        return default


async def run_round(
    round_num: int,
    num_rounds: int,
    emails_per_round: int,
    generator_service: GeneratorAgentService,
    detector_service: DetectorAgentService,
    round_id: int,
    logger: logging.Logger,
) -> list[dict]:
    results = []

    for email_num in range(1, emails_per_round + 1):
        print(f"\n   Generating email {email_num}/{emails_per_round}...")
        logger.info(f"[Round {round_num}, Email {email_num}] Generating...")

        # --- Generator (Gemini) ---
        gen_result = await generator_service.generate_email()

        try:
            gen_output = json.loads(gen_result.final_output)
        except (json.JSONDecodeError, AttributeError) as e:
            msg = f"Generator returned invalid JSON: {e}"
            print(f"   ✗ {msg}")
            logger.warning(f"[Round {round_num}, Email {email_num}] {msg}")
            save_log('warning', msg, round_id=round_id)
            results.append({"generator_agent_return_status": 0, "detector_agent_return_status": 0})
            continue

        subject      = gen_output.get('subject', '')
        from_addr    = gen_output.get('from', '')
        body         = gen_output.get('body', '')
        email_content = f"Subject: {subject}\nFrom: {from_addr}\n\n{body}"
        print(f"   ✓ Generated: [{gen_output.get('email_type', '?').upper()}] {subject}")
        logger.info(f"[Round {round_num}, Email {email_num}] Generated — type={gen_output.get('email_type')}")

        # --- Detector (Claude) ---
        det_result = await detector_service.analyze_email(email_content)

        try:
            det_output = json.loads(det_result.final_output)
        except (json.JSONDecodeError, AttributeError) as e:
            msg = f"Detector returned invalid JSON: {e}"
            print(f"   ✗ {msg}")
            logger.warning(f"[Round {round_num}, Email {email_num}] {msg}")
            save_log('warning', msg, round_id=round_id)
            results.append({"generator_agent_return_status": 1, "detector_agent_return_status": 0})
            continue

        verdict    = det_output.get('verdict', '')
        confidence = det_output.get('confidence', 0)
        print(f"   ✓ Verdict:   {verdict} ({confidence * 100:.0f}% confidence)")
        logger.info(f"[Round {round_num}, Email {email_num}] Verdict={verdict} confidence={confidence:.2f}")

        # --- Persist to PostgreSQL ---
        # Map openai-agentic field names → save_email() expected keys
        email_db_payload = {
            "generated_content":      email_content,
            "generated_subject":      subject,
            "generated_body":         body,
            "is_phishing":            gen_output.get('is_phishing', True),
            "generated_email_metadata": gen_output.get('metadata', {}),
            "detection_verdict":      verdict,
            "detection_risk_score":   det_output.get('scam_score'),
            "detection_confidence":   confidence,
            "detection_reasoning":    det_output.get('reasoning'),
            "cost":                   0.0,  # Runner.run() doesn't expose cost directly
        }
        email_id = save_email(round_id=round_id, email_result=email_db_payload)
        if email_id:
            logger.info(f"[Round {round_num}, Email {email_num}] Saved to DB — email_id={email_id}")
        else:
            msg = f"Failed to save email {email_num} to database"
            logger.warning(f"[Round {round_num}] {msg}")
            save_log('warning', msg, round_id=round_id)

        results.append({
            "generator_agent_return_status": 1,
            "detector_agent_return_status": 1,
            "email_id": email_id,
            # Generator outputs
            "email_type":        gen_output.get("email_type"),
            "subject":           subject,
            "from":              from_addr,
            "body":              body,
            "is_phishing":       gen_output.get("is_phishing"),
            "generated_metadata": gen_output.get("metadata", {}),
            # Detector outputs
            "verdict":    verdict,
            "confidence": confidence,
            "scam_score": det_output.get("scam_score"),
            "reasoning":  det_output.get("reasoning"),
            "indicators": det_output.get("indicators", []),
        })

    return results


async def main():
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Starting OpenAI Agents SDK Orchestration Session")
    logger.info("=" * 60)

    # Initialize PostgreSQL connection (Flask-SQLAlchemy via create_app)
    init_db()

    args = parse_args()

    # Resolve rounds / emails-per-round: CLI args → interactive prompt → default 1
    num_rounds = args.rounds if args.rounds and args.rounds > 0 else prompt_int("\nEnter number of rounds: ")
    emails_per_round = (
        args.emails_per_round if args.emails_per_round and args.emails_per_round > 0
        else prompt_int("Enter number of emails per round: ")
    )

    logger.info(f"Configuration: {num_rounds} rounds, {emails_per_round} emails per round")

    print("\n" + "=" * 60)
    print("OPENAI AGENTS SDK - PHISHING ORCHESTRATION")
    print(f"   Rounds: {num_rounds}  |  Emails per round: {emails_per_round}")
    print("=" * 60)

    # Instantiate services once — each creates its entity + Agent internally
    generator_service = GeneratorAgentService()
    detector_service  = DetectorAgentService()

    all_rounds: list[dict] = []

    for round_num in range(1, num_rounds + 1):
        print(f"\n{'='*60}\nROUND {round_num}/{num_rounds}\n{'='*60}")

        # Create round record in DB
        round_id = create_round(total_emails=emails_per_round, status='running')
        if not round_id:
            logger.error(f"[Round {round_num}] Failed to create round in database — skipping")
            continue

        print(f"✅ Round created with ID: {round_id}\n")
        round_start = datetime.now(UTC)

        emails = await run_round(
            round_num, num_rounds, emails_per_round,
            generator_service, detector_service,
            round_id, logger,
        )

        # Compute summary stats
        gen_ok  = sum(e.get("generator_agent_return_status", 0) for e in emails)
        det_ok  = sum(e.get("detector_agent_return_status", 0) for e in emails)
        processing_time = int((datetime.now(UTC) - round_start).total_seconds())
        detector_accuracy     = (det_ok / len(emails) * 100) if emails else 0
        generator_success_rate = (gen_ok / len(emails) * 100) if emails else 0

        update_round(
            round_id=round_id,
            status='completed',
            processed_emails=len(emails),
            detector_accuracy=detector_accuracy,
            generator_success_rate=generator_success_rate,
            processing_time=processing_time,
            total_cost=0.0,
        )

        all_rounds.append({"round_number": round_num, "round_id": round_id, "emails": emails, "total_emails": len(emails)})

        print(f"\n✅ Round {round_num} complete: {len(emails)} emails")
        print(f"   Generator successes: {gen_ok}/{len(emails)}")
        print(f"   Detector  successes: {det_ok}/{len(emails)}")
        print(f"   Processing time: {processing_time}s")
        logger.info(f"[Round {round_num}] Done — gen={gen_ok}/{len(emails)}, det={det_ok}/{len(emails)}, time={processing_time}s")

    print("\n" + "=" * 60)
    print("ORCHESTRATION COMPLETE")
    print(f"   Total rounds:           {num_rounds}")
    print(f"   Total emails generated: {num_rounds * emails_per_round}")
    print("=" * 60)
    logger.info("=" * 60)
    logger.info(f"Session complete — {num_rounds} rounds, {num_rounds * emails_per_round} emails total")
    logger.info("=" * 60)

    return {
        "total_rounds": num_rounds,
        "emails_per_round": emails_per_round,
        "total_emails": num_rounds * emails_per_round,
        "rounds": all_rounds,
    }


if __name__ == "__main__":
    asyncio.run(main())
