def run_demo(system):
    print("\n" + "="*60)
    print("  TRANSIT DESTINATION GROUPING SYSTEM — DEMO MODE")
    print("="*60)

    test_passengers = [
        # ZONE A — Door 1 (Long trip: ≥28 mins) - 13 Passengers
        ("Maria Santos",      "LRT-1", "Fernando Poe Jr.", "Baclaran"),
        ("Pedro Reyes",       "LRT-1", "Fernando Poe Jr.", "EDSA"),
        ("Jose Cruz",         "LRT-1", "Fernando Poe Jr.", "Gil Puyat"),
        ("Ana Lim",           "LRT-1", "Balintawak",       "Baclaran"),
        ("Ramon Dela Cruz",   "LRT-1", "Fernando Poe Jr.", "Libertad"),
        ("Sofia Reyes",       "LRT-1", "Fernando Poe Jr.", "Vito Cruz"),
        ("Miguel Santos",     "LRT-1", "Balintawak",       "EDSA"),
        ("Juan Aquino",       "LRT-1", "Monumento",        "Baclaran"),
        ("Elena Mendoza",     "LRT-1", "Fernando Poe Jr.", "Quirino"),
        ("Antonio Luna",      "LRT-1", "Monumento",        "Gil Puyat"),
        ("Gloria Arroyo",     "LRT-1", "Fernando Poe Jr.", "Pedro Gil"),
        ("Rodrigo Santos",    "LRT-1", "Balintawak",       "Gil Puyat"),
        ("Leni Robredo",      "LRT-1", "Fernando Poe Jr.", "United Nations"),

        # ZONE B — Door 2 (Medium-long: 14-27 mins) - 12 Passengers
        ("Grace Poe",         "LRT-1", "Fernando Poe Jr.", "Doroteo Jose"),
        ("Manuel Roxas",      "LRT-1", "Balintawak",       "Carriedo"),
        ("Cory Aquino",       "LRT-1", "Monumento",        "Central Terminal"),
        ("Ferdinand Marcos",  "LRT-1", "5th Avenue",       "Pedro Gil"),
        ("Jose Rizal",        "LRT-1", "R. Papa",          "United Nations"),
        ("Andres Bonifacio",  "LRT-1", "Abad Santos",      "Central Terminal"),
        ("Apolinario Mabini", "LRT-1", "Blumentritt",      "Pedro Gil"),
        ("Juan Luna",         "LRT-1", "Tayuman",          "Vito Cruz"),
        ("Marcelo del Pilar", "LRT-1", "Bambang",          "Quirino"),
        ("Melchora Aquino",   "LRT-1", "Doroteo Jose",     "Vito Cruz"),
        ("Emilio Aguinaldo",  "LRT-1", "Fernando Poe Jr.", "Blumentritt"),
        ("Gabriela Silang",   "LRT-1", "Balintawak",       "Bambang"),

        # ZONE C — Door 3 (Medium: 6-13 mins) - 13 Passengers
        ("Carlo Jose",        "LRT-1", "Fernando Poe Jr.", "5th Avenue"),
        ("Divine Castro",     "LRT-1", "Balintawak",       "R. Papa"),
        ("Edgar Silva",       "LRT-1", "Monumento",        "Abad Santos"),
        ("Fe Villanueva",     "LRT-1", "5th Avenue",       "Tayuman"),
        ("Gerry Almeda",      "LRT-1", "R. Papa",          "Bambang"),
        ("Helen Gamboa",      "LRT-1", "Abad Santos",      "Doroteo Jose"),
        ("Ian de Leon",       "LRT-1", "Blumentritt",      "Carriedo"),
        ("Katrina Reyes",     "LRT-1", "Tayuman",          "Central Terminal"),
        ("Jerome Garcia",     "LRT-1", "Bambang",          "United Nations"),
        ("Liza Soberano",     "LRT-1", "Doroteo Jose",     "Pedro Gil"),
        ("Mario Maurer",      "LRT-1", "Fernando Poe Jr.", "Tayuman"),
        ("Nadine Lustre",     "LRT-1", "Balintawak",       "Blumentritt"),
        ("James Reid",        "LRT-1", "Monumento",        "Carriedo"),

        # ZONE D — Door 4 (Short: 1-5 mins) - 12 Passengers
        ("Mark Dela Cruz",    "LRT-1", "Tayuman",          "Bambang"),
        ("Lea Bautista",      "LRT-1", "Abad Santos",      "Blumentritt"),
        ("Rico Santos",       "LRT-1", "Monumento",        "5th Avenue"),
        ("Tina Reyes",        "LRT-1", "Balintawak",       "Monumento"),
        ("Bong Cruz",         "LRT-1", "Fernando Poe Jr.", "Balintawak"),
        ("Nenita Garcia",     "LRT-1", "Tayuman",          "Doroteo Jose"),
        ("Ronnie Tan",        "LRT-1", "Bambang",          "Doroteo Jose"),
        ("Charity Lim",       "LRT-1", "5th Avenue",       "R. Papa"),
        ("Daniel Padilla",    "LRT-1", "Carriedo",         "Central Terminal"),
        ("Kathryn Bernardo",  "LRT-1", "Central Terminal", "United Nations"),
        ("Alden Richards",    "LRT-1", "Balintawak",       "5th Avenue"),
        ("Maine Mendoza",     "LRT-1", "5th Avenue",       "Abad Santos"),
    ]

    print("\n📋 Registering Passengers (P1 → P10)...")
    print("-"*60)
    for name, line, origin, destination in test_passengers:
        ok, msg, p = system.register_passenger(name, line, origin, destination)
        if ok:
            print(
                f"  ✓ {p.name:<15} {p.stops:>2} mins → {p.zone} | Priority: {p.priority}s")
        else:
            print(f"  ✗ {name} — {msg}")

    print("\n✅ Demo data loaded! UI is ready.")
    print("="*60 + "\n")


if __name__ == "__main__":
    from engine import TransitSystem
    system = TransitSystem()
    run_demo(system)
