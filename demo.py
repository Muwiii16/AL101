def run_demo(system):
    print("\n" + "="*60)
    print("  TRANSIT DESTINATION GROUPING SYSTEM — DEMO MODE")
    print("="*60)

    test_passengers = [
        # ZONE A — Door 1 (Long-Distance: ≥10 stops) - 10 Passengers
        ("Maria Santos",     "LRT-1", "Fernando Poe Jr.", "Baclaran"),     # 19 stops
        ("Pedro Reyes",      "LRT-1", "Fernando Poe Jr.", "EDSA"),         # 18 stops
        ("Jose Cruz",        "LRT-1", "Fernando Poe Jr.", "Gil Puyat"),    # 16 stops
        ("Ana Lim",          "LRT-1", "Balintawak",       "Baclaran"),     # 18 stops
        ("Ramon Dela Cruz",  "LRT-1", "Fernando Poe Jr.", "Libertad"),     # 17 stops
        ("Sofia Reyes",      "LRT-1", "Fernando Poe Jr.", "Vito Cruz"),     # 15 stops
        ("Miguel Santos",    "LRT-1", "Balintawak",       "EDSA"),         # 17 stops
        ("Juan Aquino",      "LRT-1", "Monumento",        "Baclaran"),     # 17 stops
        ("Elena Mendoza",    "LRT-1", "Fernando Poe Jr.", "Quirino"),      # 14 stops
        ("Antonio Luna",     "LRT-1", "Monumento",        "Gil Puyat"),    # 14 stops

        # ZONE B — Door 2 (Medium-Distance: 5–9 stops) - 10 Passengers
        ("Grace Poe",        "LRT-1", "Fernando Poe Jr.", "Doroteo Jose"),  # 9 stops
        ("Manuel Roxas",     "LRT-1", "Balintawak",       "Carriedo"),     # 9 stops
        ("Cory Aquino",      "LRT-1", "Monumento",
         "Central Terminal"),  # 9 stops
        ("Ferdinand Marcos", "LRT-1", "5th Avenue",       "Pedro Gil"),    # 10 stops
        ("Jose Rizal",       "LRT-1", "R. Papa",
         "United Nations"),  # 8 stops
        ("Andres Bonifacio", "LRT-1", "Abad Santos",
         "Central Terminal"),  # 6 stops
        ("Apolinario Mabini", "LRT-1", "Blumentritt",      "Pedro Gil"),    # 7 stops
        ("Juan Luna",        "LRT-1", "Tayuman",          "Vito Cruz"),    # 8 stops
        ("Marcelo del Pilar", "LRT-1", "Bambang",          "Quirino"),      # 6 stops
        ("Melchora Aquino",  "LRT-1", "Doroteo Jose",     "Vito Cruz"),    # 6 stops

        # ZONE C — Door 3 (Short-Distance: 3–4 stops) - 10 Passengers
        ("Carlo Jose",       "LRT-1", "Fernando Poe Jr.", "5th Avenue"),   # 3 stops
        ("Divine Castro",    "LRT-1", "Balintawak",       "R. Papa"),      # 3 stops
        ("Edgar Silva",      "LRT-1", "Monumento",        "Abad Santos"),  # 3 stops
        ("Fe Villanueva",    "LRT-1", "5th Avenue",       "Tayuman"),      # 4 stops
        ("Gerry Almeda",     "LRT-1", "R. Papa",          "Bambang"),      # 4 stops
        ("Helen Gamboa",     "LRT-1", "Abad Santos",      "Doroteo Jose"),  # 4 stops
        ("Ian de Leon",      "LRT-1", "Blumentritt",      "Carriedo"),     # 4 stops
        ("Katrina Reyes",    "LRT-1", "Tayuman",
         "Central Terminal"),  # 4 stops
        ("Jerome Garcia",    "LRT-1", "Bambang",
         "United Nations"),  # 4 stops
        ("Liza Soberano",    "LRT-1", "Doroteo Jose",     "Pedro Gil"),    # 4 stops

        # ZONE D — Door 4 (Immediate/Local: 1–2 stops) - 10 Passengers
        ("Mark Dela Cruz",   "LRT-1", "Tayuman",          "Bambang"),      # 1 stop
        ("Lea Bautista",     "LRT-1", "Abad Santos",      "Blumentritt"),  # 2 stops
        ("Rico Santos",      "LRT-1", "Monumento",        "5th Avenue"),   # 1 stop
        ("Tina Reyes",       "LRT-1", "Balintawak",       "Monumento"),    # 1 stop
        ("Bong Cruz",        "LRT-1", "Fernando Poe Jr.", "Balintawak"),   # 1 stop
        ("Nenita Garcia",    "LRT-1", "Tayuman",          "Doroteo Jose"),  # 2 stops
        ("Ronnie Tan",       "LRT-1", "Bambang",          "Doroteo Jose"),  # 1 stop
        ("Charity Lim",      "LRT-1", "5th Avenue",       "R. Papa"),      # 2 stops
        ("Daniel Padilla",   "LRT-1", "Carriedo",
         "Central Terminal"),  # 1 stop
        ("Kathryn Bernardo", "LRT-1", "Central Terminal", "United Nations"),  # 1 stop
    ]

    print("\n📋 Registering Passengers (P1 → P10)...")
    print("-"*60)
    for name, line, origin, destination in test_passengers:
        ok, msg, p = system.register_passenger(name, line, origin, destination)
        if ok:
            print(
                f"  ✓ {p.name:<15} {p.stops:>2} stops → {p.zone} | Priority: {p.priority}")
        else:
            print(f"  ✗ {name} — {msg}")

    print("\n✅ Demo data loaded! UI is ready.")
    print("="*60 + "\n")


if __name__ == "__main__":
    from engine import TransitSystem
    system = TransitSystem()
    run_demo(system)
