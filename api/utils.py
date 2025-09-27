# utils.py
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.urls import reverse
from django.conf import settings

logger = logging.getLogger(__name__)

def send_verification_email(request, user_profile, context_data=None):
    """
    Send verification email to user
    
    Args:
        request: Django request object for building absolute URI
        user_profile: UserProfile instance
        context_data: Optional dict of additional context data
    
    Returns:
        tuple: (success: bool, error_message: str or None)
    """
    try:
        user = user_profile.user
        
        subject = 'Verify Your Email - Social Network'
        from_email = settings.EMAIL_HOST_USER
        to_email = user.email
        
        # verification URL
        verification_url = request.build_absolute_uri(
            reverse('verify_email', kwargs={'token': user_profile.email_verification_token})
        )
        
        # template context
        context = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'verification_url': verification_url
        }
        
        if context_data:
            context.update(context_data)
        
        # email template
        template = get_template('registration/verification_email.html')
        html_content = template.render(context)
        
        # send email
        msg = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        
        logger.info(f'Verification email sent successfully to {to_email}')
        return True, None
        
    except Exception as e:
        error_msg = f'Failed to send verification email to {user_profile.user.email}: {str(e)}'
        logger.error(error_msg, exc_info=True)
        return False, error_msg


class EmailService:
    """Service class for handling various email operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def send_template_email(self, request, template_name, subject, to_email, context, from_email=None):
        """
        Generic method to send templated emails
        
        Args:
            request: Django request object
            template_name: Path to email template
            subject: Email subject
            to_email: Recipient email
            context: Template context dict
            from_email: Sender email (optional)
        
        Returns:
            tuple: (success: bool, error_message: str or None)
        """
        try:
            if from_email is None:
                from_email = settings.EMAIL_HOST_USER or 'noreply@socialnetwork.com'
            
            template = get_template(template_name)
            html_content = template.render(context)
            
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            self.logger.info(f'Email "{subject}" sent successfully to {to_email}')
            return True, None
            
        except Exception as e:
            error_msg = f'Failed to send email "{subject}" to {to_email}: {str(e)}'
            self.logger.error(error_msg, exc_info=True)
            return False, error_msg
    
    def send_verification_email(self, request, user_profile):
        """Send email verification email"""
        user = user_profile.user
        
        verification_url = request.build_absolute_uri(
            reverse('verify_email', kwargs={'token': user_profile.email_verification_token})
        )
        
        context = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'verification_url': verification_url
        }
        
        return self.send_template_email(
            request=request,
            template_name='registration/verification_email.html',
            subject='Verify Your Email - Social Network',
            to_email=user.email,
            context=context
        )

# mock post messages
sample_posts = [
    "Finally beat my chess mentor in a proper game last night! We've been playing weekly for about six months now, and I could see the improvement happening slowly.\n\nWhat really made the difference was learning to think three moves ahead instead of just reacting to threats. The tactical patterns I've been studying finally clicked into place.\n\nCelebrated with my favorite victory dance in the kitchen. My cat was not impressed, but I couldn't contain the excitement!",
    "Spent the afternoon at the local pool hall and had one of those magical sessions where everything just flows. My break was crisp, my positioning was on point.\n\nThere's something meditative about the geometry of pool - calculating angles, planning your next three shots while lining up the current one. It's like chess but with physics.\n\nEnded up winning five games straight against some regulars. They weren't too happy, but bought me a drink anyway. Great community at that place.",
    "Discovered a new jazz club downtown and the live music absolutely blew me away. The pianist had this incredible way of taking familiar melodies and making them feel completely fresh.\n\nI've been trying to learn piano myself, but watching a master at work reminded me how much further I have to go. The way they improvised was like watching someone paint with sound.\n\nAlready booked tickets for next week's show. Sometimes you need to step away from screens and remember what real artistry looks like.",
    "My salsa dancing classes are finally paying off! Last night's social dance was the first time I felt confident leading without constantly thinking about my feet.\n\nThe breakthrough came when I stopped trying to memorize complex patterns and just focused on connecting with the music and my partner. Dance is more about feeling than thinking.\n\nMy instructor says I'm ready to try bachata next month. Nervous but excited to expand my repertoire and meet more people in the dance community.",
    "Finished my first proper charcoal portrait today after weeks of practice sketches. Drawing realistic faces is so much harder than I expected when I started this hobby.\n\nThe biggest challenge was getting the proportions right - eyes too far apart, nose too long, mouth too small. But slowly I'm training my eye to see what's actually there.\n\nMy neighbor agreed to be my next subject. She has these amazing laugh lines that I think will be fun to capture. Drawing people is like telling their story through shadows.",
    "Watched the World Snooker Championship last weekend and I'm completely hooked. The precision these players have is absolutely mind-blowing - every shot planned four balls ahead.\n\nDecided to try snooker myself at the club yesterday. Let's just say watching and doing are very different things! Couldn't even pot a red consistently, let alone think about position play.\n\nBut the challenge is addictive. Booked lessons with the club pro starting next week. Something about the tactical depth really appeals to me.",
    "My guitar practice is starting to pay off after months of sore fingertips and frustrated attempts at bar chords. Finally played through an entire song without stopping!\n\nIt was just 'Wonderwall' but hey, we all start somewhere. The muscle memory is finally developing and chord changes are becoming smoother.\n\nThinking about joining the informal jam sessions they have at the community center. Terrifying but probably exactly what I need to push to the next level.",
    "Attended my first chess tournament last Saturday. Got completely crushed in most games but learned more in one day than months of casual play.\n\nFacing opponents who actually know opening theory exposed all the gaps in my knowledge. But everyone was incredibly welcoming and happy to analyze games afterward.\n\nAlready signed up for next month's tournament. Win or lose, there's something special about the focused silence of competitive chess that I find addictive.",
    "Started taking watercolor classes and I'm discovering how different it is from the pencil sketching I'm used to. Water has its own mind and doesn't always cooperate!\n\nThe instructor keeps saying 'embrace the accidents' - let the paint flow and work with happy mistakes instead of fighting them. It's teaching me to be less controlling.\n\nPainted a simple landscape yesterday that actually looked like something recognizable. Small victories, but they feel huge when you're learning something completely new.",
    "Hit my first 147 break in snooker practice today! Well, not in a real game, but I managed to pot all the balls in the right sequence during solo practice.\n\nTook me about two hours and countless attempts, but when that black ball finally dropped, I may have whooped loud enough to disturb the entire club.\n\nThe old-timers just smiled and nodded. Apparently everyone remembers their first maximum, even if it's just in practice. Now to try it under actual pressure!"
]

# mock users
users_data = [
    {'username': 'alice_dev', 'email': 'alice@example.com', 'first_name': 'Alice', 'last_name': 'Johnson'},
    {'username': 'bob_coder', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Smith'}
]
