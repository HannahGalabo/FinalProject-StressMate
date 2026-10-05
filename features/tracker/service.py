from features.tracker.model import StressTier, StressRecord

class StressService:
    TIERS = {
        "Level Green": StressTier(
            code="GREEN",
            status="Low Stress (Calm & Balanced)",
            insight="You are feeling steady and managing your load well.",
            task="Keep momentum: organize your desk, drink water, or take a short walk.",
            color_hex="#16A34A"
        ),
        "Level Yellow": StressTier(
            code="YELLOW",
            status="Moderate Stress (Feeling Pressured)",
            insight="Deadlines or tasks are piling up, but it is manageable.",
            task="5-Minute Reset: Step away from your screen, stretch, and write down your top priority.",
            color_hex="#CA8A04"
        ),
        "Level Orange": StressTier(
            code="ORANGE",
            status="High Stress (Overwhelmed / Exhausted)",
            insight="Your mind and body are signaling for a pause. It is okay to step back.",
            task="Emergency Pause: 4-7-8 breathing exercise, eat a snack, or talk to a friend. Work can wait 15 minutes.",
            color_hex="#EA580C"
        ),
        "Level Red": StressTier(
            code="RED",
            status="Critical Stress (Extremely Stressed & Overwhelmed)",
            insight="Your mind and body are signaling a complete overload. Continuing right now is counterproductive.",
            task="Total Stop: Step away from all work. Do 3 minutes of grounding, drink cold water, and connect with someone.",
            color_hex="#DC2626"
        )
    }

    HELP_RESOURCES = {
        "physical": (
            "PHYSICAL HELP & RECOVERY\n"
            "• Nutrition & Hydration: Drink a glass of water. Eat a nutritious snack.\n"
            "• Sleep & Rest: Ensure 7-8 hours of sleep. Take a 15-minute quiet pause if exhausted.\n"
            "• Movement: Walk outside for 10 minutes or stretch.\n"
            "• Breathing: Inhale 4s, hold 7s, exhale 8s.\n"
            "• Warning Signs: Headaches or tight chest signal an urgent need to pause."
        ),
        "emotional": (
            "EMOTIONAL HELP & RESILIENCE\n"
            "• One Day at a Time: Focus only on what you can control right now.\n"
            "• Reframe Thoughts: Replace 'I can't handle this' with 'I am taking it one step at a time.'\n"
            "• Talk It Out: Share how you feel with a trusted friend.\n"
            "• Accept Feelings: It's okay to feel overwhelmed.\n"
            "• Lower Perfections: Focus on progress rather than perfection."
        ),
        "spiritual": (
            "SPIRITUAL HELP & PEACE\n"
            "• Meditation: Spend 5 minutes in quiet stillness or prayer.\n"
            "• Reflection: Read an uplifting passage.\n"
            "• Acts of Kindness: Shift focus by helping someone else.\n"
            "• Gratitude: Write down 3 small things you are thankful for.\n"
            "• Remember Your Worth: Your value is not defined by productivity."
        )
    }

    def __init__(self, repository):
        self.repo = repository

    def get_tier_by_label(self, label: str) -> StressTier:
        return self.TIERS.get(label, self.TIERS["Level Green"])

    def get_tier_by_code(self, code: str) -> StressTier:
        for t in self.TIERS.values():
            if t.code == code:
                return t
        return self.TIERS["Level Green"]

    def log_stress(self, user_id: int, dropdown_label: str, note: str):
        tier = self.get_tier_by_label(dropdown_label)
        rec = StressRecord.create_new(user_id, tier.code, tier.task, note)
        return self.repo.create(rec)

    def get_user_history(self, user_id: int):
        return self.repo.get_all_by_user(user_id)

    def update_log(self, record_id: int, user_id: int, new_code: str, new_note: str):
        tier = self.get_tier_by_code(new_code)
        self.repo.update(record_id, user_id, tier.code, tier.task, new_note)

    def delete_log(self, record_id: int, user_id: int):
        self.repo.delete(record_id, user_id)