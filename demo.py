def run_demo(system):   # ← accepts existing system
    print("\n" + "="*60)
    print("  TRANSIT DESTINATION GROUPING SYSTEM — DEMO MODE")
    print("="*60)

    test_passengers = [
        # ZONE A — Door 1 (≥10 stops) — 3 per car = 15 total
        ("Maria Santos",     "LRT-1", "Fernando Poe Jr.", "Baclaran"),     # 19 stops
        ("Maria Santos",     "LRT-1", "Fernando Poe Jr.", "Baclaran"),
        ("Maria Santos",     "LRT-1", "Fernando Poe Jr.", "Baclaran"),
        ("Maria Santos",     "LRT-1", "Fernando Poe Jr.", "Baclaran"),
        ("Maria Santos",     "LRT-1", "Fernando Poe Jr.", "Baclaran"),
        ("Pedro Reyes",      "LRT-1", "Monumento",        "Baclaran"),     # 17 stops
        ("Jose Cruz",        "LRT-1", "Fernando Poe Jr.", "Gil Puyat"),    # 16 stops
        ("Ana Lim",          "LRT-1", "Balintawak",       "Baclaran"),     # 18 stops
        ("Ramon Dela Cruz",  "LRT-1", "Fernando Poe Jr.", "Libertad"),     # 17 stops
        ("Sofia Reyes",      "LRT-1", "Fernando Poe Jr.", "EDSA"),         # 18 stops
        ("Miguel Santos",    "LRT-1", "Fernando Poe Jr.", "Vito Cruz"),    # 15 stops
        ("Elena Garcia",     "LRT-1", "Balintawak",       "Gil Puyat"),    # 15 stops
        ("Roberto Cruz",     "LRT-1", "Fernando Poe Jr.",
         "United Nations"),  # 12 stops
        ("Isabella Tan",     "LRT-1", "Monumento",        "Gil Puyat"),    # 14 stops
        ("Antonio Reyes",    "LRT-1", "Fernando Poe Jr.", "Pedro Gil"),    # 13 stops
        ("Gabriela Lim",     "LRT-1", "Balintawak",       "Libertad"),     # 16 stops

        # ZONE B — Door 2 (6-9 stops)
        ("Carlo Tan",        "LRT-1", "Fernando Poe Jr.", "Doroteo Jose"),  # 9 stops
        ("Lea Villanueva",   "LRT-1", "Monumento",        "Pedro Gil"),    # 8 stops
        ("Marco Garcia",     "LRT-1", "Balintawak",       "Carriedo"),     # 8 stops
        ("Nina Santos",      "LRT-1", "Fernando Poe Jr.", "Bambang"),      # 8 stops
        ("Diego Reyes",      "LRT-1", "Monumento",
         "United Nations"),  # 7 stops
        ("Camille Cruz",     "LRT-1", "Fernando Poe Jr.", "Carriedo"),     # 10 stops
        ("Rafael Tan",       "LRT-1", "Balintawak",       "Doroteo Jose"),  # 7 stops
        ("Patricia Lim",     "LRT-1", "Fernando Poe Jr.", "Abad Santos"),  # 6 stops
        ("Vincent Santos",   "LRT-1", "Monumento",        "Carriedo"),     # 8 stops

        # ZONE C — Door 3 (3-5 stops)
        ("Rosa Garcia",      "LRT-1", "Fernando Poe Jr.", "Blumentritt"),  # 5 stops
        ("Luis Reyes",       "LRT-1", "Monumento",        "Doroteo Jose"),  # 5 stops
        ("Clara Tan",        "LRT-1", "Balintawak",       "R. Papa"),      # 3 stops
        ("Diego Cruz",       "LRT-1", "Fernando Poe Jr.", "Tayuman"),      # 4 stops
        ("Bianca Santos",    "LRT-1", "Monumento",        "Blumentritt"),  # 3 stops
        ("Francis Lim",      "LRT-1", "Fernando Poe Jr.", "5th Avenue"),   # 3 stops
        ("Katrina Reyes",    "LRT-1", "Balintawak",       "Blumentritt"),  # 4 stops
        ("Jerome Garcia",    "LRT-1", "Monumento",        "R. Papa"),      # 4 stops

        # ZONE D — Door 4 (1-2 stops)
        ("Mark Dela Cruz",   "LRT-1", "Tayuman",          "Bambang"),      # 1 stop
        ("Lea Bautista",     "LRT-1", "Abad Santos",      "Blumentritt"),  # 2 stops
        ("Rico Santos",      "LRT-1", "Monumento",        "5th Avenue"),   # 1 stop
        ("Tina Reyes",       "LRT-1", "Balintawak",       "Monumento"),    # 1 stop
        ("Bong Cruz",        "LRT-1", "Fernando Poe Jr.", "Balintawak"),   # 1 stop
        ("Nenita Garcia",    "LRT-1", "Tayuman",          "Doroteo Jose"),  # 2 stops
        ("Ronnie Tan",       "LRT-1", "Bambang",          "Doroteo Jose"),  # 1 stop
        ("Charity Lim",      "LRT-1", "5th Avenue",       "R. Papa"),      # 2 stops
    ]

    print("\n📋 Registering Passengers...")
    for name, line, origin, destination in test_passengers:
        ok, msg, p = system.register_passenger(name, line, origin, destination)
        if ok:
            print(f"  ✓ {p.name:<20} {p.stops:>2} stops → {p.zone}")
        else:
            print(f"  ✗ {name} — {msg}")

    print("\n✅ Demo data loaded! UI is ready.")
    print("="*60 + "\n")


# this only runs when you do: python demo.py directly
if __name__ == "__main__":
    from engine import TransitSystem
    system = TransitSystem()
    run_demo(system)
