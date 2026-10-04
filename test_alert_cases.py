from alert_monitor import (
    classify_alert,
    is_alert_candidate,
    validate_alert_row,
)


def make_row(
    container_id="TEST001",
    route="Pune-Mumbai",
    temperature=37.0,
    humidity=82.0,
    vibration=0.25,
    distance=150,
    spoilage_risk="high",
    estimated_time=12,
    action="monitor closely",
    routing="reroute recommended",
    priority="high",
    reroute_required=1,
):
    return {
        "container_id": container_id,
        "route": route,
        "temperature": temperature,
        "humidity": humidity,
        "vibration": vibration,
        "distance_to_market_km": distance,
        "spoilage_risk": spoilage_risk,
        "estimated_time_to_spoilage_hours": estimated_time,
        "recommended_action": action,
        "routing_recommendation": routing,
        "arbitrage_priority": priority,
        "reroute_required": reroute_required,
    }


def test_opportunity_detected():
    row = make_row(
        container_id="TEST001",
        spoilage_risk="high",
        reroute_required=1,
    )

    return (
        is_alert_candidate(row)
        and classify_alert(row) == "high"
    )


def test_no_opportunity():
    row = make_row(
        container_id="TEST002",
        temperature=25.0,
        humidity=55.0,
        spoilage_risk="low",
        action="normal",
        routing="continue current route",
        priority="low",
        reroute_required=0,
    )

    return (
        not is_alert_candidate(row)
        and classify_alert(row) == "none"
    )


def test_invalid_data():
    row = make_row(
        container_id="TEST003",
        temperature=None,
        spoilage_risk="high",
        reroute_required=1,
    )

    return (
        not validate_alert_row(row)
        and classify_alert(row) == "invalid"
        and not is_alert_candidate(row)
    )


def test_multiple_opportunities():
    rows = [
        make_row(
            container_id="TEST004",
            spoilage_risk="critical",
            priority="urgent",
            reroute_required=1,
        ),
        make_row(
            container_id="TEST005",
            spoilage_risk="high",
            priority="high",
            reroute_required=1,
        ),
        make_row(
            container_id="TEST006",
            spoilage_risk="high",
            priority="high",
            reroute_required=1,
        ),
    ]

    detected = [
        row for row in rows
        if is_alert_candidate(row)
    ]

    return len(detected) == 3


def run_test(name, test_function):
    try:
        result = test_function()

        if result:
            print(f"PASS: {name}")
            return True

        print(f"FAIL: {name}")
        return False

    except Exception as exc:
        print(f"ERROR: {name} -> {exc}")
        return False


def main():
    tests = [
        ("Opportunity detected", test_opportunity_detected),
        ("No opportunity", test_no_opportunity),
        ("Invalid data", test_invalid_data),
        ("Multiple opportunities", test_multiple_opportunities),
    ]

    passed = 0

    for name, test_function in tests:
        if run_test(name, test_function):
            passed += 1

    print()
    print(f"Tests passed: {passed}/{len(tests)}")

    if passed == len(tests):
        print("All Day 4 alert tests passed.")
    else:
        print("Some Day 4 alert tests failed.")


if __name__ == "__main__":
    main()