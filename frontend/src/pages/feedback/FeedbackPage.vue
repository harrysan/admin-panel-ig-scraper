<template>
  <div>
    <div class="container-lg py-3 mt-4">
      <div class="container shadow p-3 mb-5 bg-body rounded px-2 py-1">
        <h3 class="font-semibold text-dark mt-2 mb-2 p-3">Feedback</h3>
        <div class="row p-3 background-grey">
          <div class="col">Got a feedback? Please let us know.</div>
        </div>
        <form class="p-3" @submit.prevent="sendEmail">
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input
              type="text"
              class="form-control"
              id="name"
              v-model.trim="name"
              placeholder="Your name"
            />
          </div>
          <div class="mb-3">
            <label for="message" class="form-label">Message</label>
            <input
              type="text"
              class="form-control"
              id="message"
              v-model.trim="message"
              placeholder="Input your message here"
            />
          </div>
          <base-button>Send</base-button>
        </form>
        <div class="mt-1 p-3" v-if="isSend">
          Message successfuly send. Thanks for your feedback :) !
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
// import emailjs from "@emailjs/browser";

export default {
  setup() {
    const name = ref("");
    const message = ref("");
    const isSend = ref(false);

    async function sendEmail() {
      var template_params = {
        from_name: name.value,
        message: message.value,
        to_name: "Admin",
      };

      var data = {
        service_id: process.env.VUE_APP_SERVICEID,
        template_id: process.env.VUE_APP_TEMPLATEID,
        user_id: process.env.VUE_APP_PUBLICKEY,
        template_params: template_params,
        accessToken: process.env.VUE_APP_PRIVATEKEY,
      };

      try {
        await fetch(`https://api.emailjs.com/api/v1.0/email/send`, {
          method: "POST",
          body: JSON.stringify(data),
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        });

        isSend.value = true;
        setTimeout(() => {
          isSend.value = false;
        }, 3000);

        name.value = "";
        message.value = "";
      } catch (error) {
        console.log(error);
      }
    }

    return { name, message, sendEmail, isSend };
  },
};
</script>
