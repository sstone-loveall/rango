from datetime import datetime


class Visits:
    def __init__(self, request):
        self.request = request

    def get_visits_count_from_session(self):
        visits = self.request.session.get('visits')
        if not visits:
            visits = 1

        return visits

    def get_last_visit_date_from_session(self):
        last_visit = self.request.session.get('last_visit')
        if last_visit:
            last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        else:
            last_visit_time = str(datetime.now())

        return last_visit_time
