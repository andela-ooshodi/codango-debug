from celery.task import task
from celery.utils.log import get_task_logger
from account.emails import SendGrid
from resources.models import Resource
from django.db.models import Count
from codango.settings.base import CODANGO_EMAIL
from django.template import Context, loader
from django.core.urlresolvers import reverse

logger = get_task_logger(__name__)


@task
def send_recent_posts(recipient):

    # Top 5 posts on Codango
    popular_posts = Resource.objects.annotate(
        num_comments=Count('comments')).annotate(
        num_votes=Count('votes')).order_by(
        '-num_comments', '-num_votes')[:5]

    # URL to Codango
    codango_url = "http://localhost:8000{}".format(reverse('index'))

    # Compose the email
    message = SendGrid.compose(
        sender='Codango <{}>'.format(CODANGO_EMAIL),
        recipient=recipient,
        subject="Top Posts on Codango",
        text=None,
        html=loader.get_template(
            'resources/popular-post-updates.html'
        ).render(Context({
            'popular_posts': popular_posts,
            'codango_url': codango_url
        }))
    )

    # send email
    response = SendGrid.send(message)
    logger.info("Sent Codango's top posts")
    return response
