import json

class StoryManager:
    def __init__(self, story_file):
        with open(story_file, 'r', encoding='utf-8') as f:
            self.story_data = json.load(f)
        self.current_scene = "start"

    def get_scene(self):
        return self.story_data["scenes"][self.current_scene]

    def set_scene(self, scene_id):
        if scene_id in self.story_data["scenes"]:
            self.current_scene = scene_id
        else:
            raise ValueError(f"Scene '{scene_id}' not found!")