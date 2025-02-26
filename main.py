from story_manager import StoryManager
from io_handle import InputHandler
from gen_support import GeminiAI

class GameEngine:
    def __init__(self, story_file, api_key):
        self.story = StoryManager(story_file)
        self.input_handler = InputHandler()
        self.ai = GeminiAI(api_key)

    def run(self):
        while True:
            scene = self.story.get_scene()
            self.input_handler.display_text(scene["text"])

            if "use_ai" in scene and scene["use_ai"]:
                ai_prompt = "어두운 숲에서 길을 잃은 모험가에게 조언을 주는 이야기를 생성해줘"
                ai_story = self.ai.generate_story(ai_prompt)
                self.input_handler.display_text(ai_story)
                break  # AI 후 종료 (필요 시 수정)

            if not scene["choices"]:
                self.input_handler.display_text("게임 종료!")
                break

            self.input_handler.display_choices(scene["choices"])
            choice_idx = self.input_handler.get_choice(scene["choices"])
            next_scene = scene["choices"][choice_idx]["next_scene"]
            self.story.set_scene(next_scene)

if __name__ == "__main__":
    story_file = "story.json"  # JSON 파일 경로
    api_key = "test"  # 실제 Gemini API 키로 교체
    game = GameEngine(story_file, api_key)
    game.run()