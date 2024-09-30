from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    RecaptchaChallengeForm,
    ReloginAttemptExceeded,
    SelectContactPointRecoveryForm,
)
import time

class HandleError:
    """We return the client class, in which we automatically handle exceptions
    You can move the "handle_exception" above or into an external module
    """
    def handle_exception(self, client, e):
        if isinstance(e, BadPassword):
            client.logger.exception(e)
            # client.set_proxy(self.next_proxy().href)
            if client.relogin_attempt > 0:
                # self.freeze(str(e), days=7)
                print("relogin attempt exceeded...")
                raise ReloginAttemptExceeded(e)
            # client.settings = self.rebuild_client_settings()
            # return self.update_client_settings(client.get_settings())
        elif isinstance(e, LoginRequired):
            print("relogin required...")
            client.logger.exception(e)
            client.relogin()
            # return self.update_client_settings(client.get_settings())
        elif isinstance(e, ChallengeRequired):
            # api_path = client.last_json.get("challenge", {}).get("api_path")
            # if api_path == "/challenge/":
            #     client.set_proxy(self.next_proxy().href)
            #     client.settings = self.rebuild_client_settings()
            #     client.settings = 
            # else:
                try:
                    print("try challenge resolve...")
                    client.challenge_resolve(client.last_json)
                except ChallengeRequired as e:
                    # self.freeze("Manual Challenge Required", days=2)
                    raise e
                except (
                    ChallengeRequired,
                    SelectContactPointRecoveryForm,
                    RecaptchaChallengeForm,
                ) as e:
                    # self.freeze(str(e), days=4)
                    raise e
                # self.update_client_settings(client.get_settings())
            # return True
        elif isinstance(e, FeedbackRequired):
            message = client.last_json["feedback_message"]
            if "This action was blocked. Please try again later" in message:
                # self.freeze(message, hours=12)
                print("This action was blocked. Sleep for 12 hour...")
                time.sleep(43200)
                # client.settings = self.rebuild_client_settings()
                # return self.update_client_settings(client.get_settings())
            elif "We restrict certain activity to protect our community" in message:
                # 6 hours is not enough
                print("We restrict certain activity. Sleep for 12 hour...")
                time.sleep(43200)
                # self.freeze(message, hours=12)
            elif "Your account has been temporarily blocked" in message:
                """
                Based on previous use of this feature, your account has been temporarily
                blocked from taking this action.
                This block will expire on 2020-03-27.
                """
                print("Your account has been temporarily blocked. Sleep for 12 hour...")
                time.sleep(43200)
        elif isinstance(e, PleaseWaitFewMinutes):
            # self.freeze(str(e), hours=1)
            print("PleaseWaitFewMinutes. Sleep for 1 hour...")
            time.sleep(3600)
            # self.login_user()
        raise e
