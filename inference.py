import random

class FocusAI:
    @staticmethod
    def decide(energy):
        if energy < 40:
            return "Break", "🚨 DANGER: Energy is critical. Break required."
        if random.random() < 0.2:
            return "Break", "☕ AI Advice: Take a micro-break to maintain long-term focus."
        return "Work", "🚀 AI Advice: You are in the 'Flow State'. Keep working."
