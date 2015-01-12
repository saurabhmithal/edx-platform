"""Payment and verification pages"""

from urllib import urlencode
from bok_choy.page_object import PageObject, unguarded
from bok_choy.promise import Promise, EmptyPromise
from . import BASE_URL
from .dashboard import DashboardPage


class SplitPaymentAndVerificationFlow(PageObject):
    """Interact with the split payment and verification flow.

    These pages are currently hidden behind the feature flag
    `SEPARATE_VERIFICATION_FROM_PAYMENT`, which is enabled in
    the Bok Choy settings.

    When enabled, the flow can be accessed at the following URLs:
        `/verify_student/start-flow/{course}/`
        `/verify_student/upgrade/{course}/`
        `/verify_student/verify-later/{course}/`
        `/verify_student/payment-confirmation/{course}/`

    Users can reach the flow when attempting to enroll in a course's verified
    mode, either directly from the track selection page, or by upgrading from
    the honor mode. Users can also reach the flow when attempting to complete
    a deferred verification, or when attempting to view a receipt corresponding
    to an earlier payment.
    """
    def __init__(self, browser, course_id, start_page='start-flow'):
        """Initialize the page.

        Arguments:
            browser (Browser): The browser instance.
            course_id (unicode): The course in which the user is enrolling.

        Keyword Arguments:
            start_page (str): Whether to start on the login or register page.

        Raises:
            ValueError
        """
        super(CombinedLoginAndRegisterPage, self).__init__(browser)
        self._course_id = course_id

        if start_page not in ['start-flow', 'upgrade', 'verify-later', 'payment-confirmation']:
            raise ValueError(
                "Start page must be either 'start-flow', 'upgrade', 'verify-later', or 'payment-confirmation'."
            )
        self._start_page = start_page

    @property
    def url(self):
        """Return the URL corresponding to the initial position in the flow."""
        url = "{base}/verify_student/{entry_point}/{course}".format(
            base=BASE_URL,
            entry_point=self._start_page,
            course=self._course_id
        )

        return url
