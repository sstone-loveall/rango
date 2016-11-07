from datetime import datetime


class Visits:
    def __init__(self, request):
        self.request = request

    def get_visits_count(self):
        visits = self.request.session.get('visits')
        if not visits:
            visits = 1

        return visits

    def get_last_visit_date(self):
        last_visit = self.request.session.get('last_visit')
        if not last_visit:
            last_visit_time = last_visit.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            last_visit_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        return last_visit_time

    def update_visits_session(self, visit_count, last_visit):
        reset_last_visit_time = False

        if visit_count:
            if last_visit:
                # if it's been more than a day since the last visit
                if (datetime.now() - last_visit).days > 0:
                    visit_count += 1
                    reset_last_visit_time = True
            else:
                reset_last_visit_time = True
        else:
            # session value doesn't exist, so flag that it should be set
            reset_last_visit_time = True

        if reset_last_visit_time:
            self.request.session['last_visit'] = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            self.request.session['visits'] = visit_count

