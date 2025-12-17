import openai

class AgileAgent:

    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def create_user_story(self, feature_description):
        """

        Parameters
        ----------
        feature_description :

        Returns
        -------

        """
        prompt = f"""
        Tu es un Product Owner et Scrum Master.
        Crée une user story complète avec :
        - Titre
        - Description
        - Critères d'acceptation
        - Tâches techniques (frontend, backend, data)
        Basé sur cette idée : {feature_description}
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        story = response['choices'][0]['message']['content']
        return story
