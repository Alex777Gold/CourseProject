new Vue({
  el: "#app",
  data: {
    subscribe: true,
    unsubscribe: true,
    csrfToken: "{{ csrf_token }}",
    msg: "",
    errorMsg: "",
    csrfToken: "",
  },
  created() {
    // Отримати CSRF-токен з мета-тега
    this.csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  },
  methods: {
    submitForm(missionId, actionType) {
      const formData = new FormData();
      formData.append("mission_id", missionId);
      formData.append("action_type", actionType);
      formData.append("csrfmiddlewaretoken", this.csrfToken);

      fetch(`/${actionType}/${missionId}/`, {
        method: "POST",
        body: formData,
        headers: {
          'X-CSRFToken': this.csrfToken
        }
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            this.msg = data.msg;
            if (actionType === 'unsubscribe') {
              window.location.reload();
            }
          } else {
            this.errorMsg = data.msg;
          }
          alert(data.msg);
        })
        .catch((error) => {
          console.error("Request error:", error);
          this.errorMsg = "An error occurred";
          alert(this.errorMsg);
        });
    },
  },
});
