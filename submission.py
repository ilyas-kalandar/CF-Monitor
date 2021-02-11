class Submission:
    def __init__(self, problem_name, rating, programming_lang, verdict, creation_time, contest_id):
        self.problem_name = problem_name
        self.rating = rating
        self.programming_lang = programming_lang
        self.verdict = verdict
        self.creation_time = creation_time
        self.contest_id = contest_id

    def __repr__(self):
        return f"Submission: Problem-Name: {self.problem_name}, verdict: {self.verdict}"
