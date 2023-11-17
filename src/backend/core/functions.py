from django.db.models import Avg

from towin.models import Feedback


def avg_towtruck_score(instance):
    """
    Рассчет средней оценки эвакуатора.
    """

    scores = Feedback.objects.filter(order__tow_truck=instance)
    if not scores:
        return None

    return scores.aggregate(Avg('score'))['score__avg']
