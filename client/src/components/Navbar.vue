<template>
  <main
    class="
      d-flex
      justify-content-between
      align-items-center
      bg-primary-subtle
      p-2
    "
  >
    <h2 class="fs-3 fw-bold m-0 ms-5 text-decoration-none">Kanban</h2>
    <section v-if="type === 'Export'">
      <router-link to="/dashboard" class="btn btn-primary me-3"
        >Dashboard</router-link
      >
      <button type="button" class="btn btn-danger me-5" @click="signout">
        Signout
      </button>
    </section>
    <section v-else>
      <button
        type="button"
        class="btn btn-primary me-3"
        data-bs-toggle="modal"
        data-bs-target="#staticBackdropList"
      >
        Add List
      </button>
      <router-link to="/export" class="btn btn-primary me-3"
        >Data Management</router-link
      >
      <router-link to="/summary" class="btn btn-primary me-3"
        >Summary</router-link
      >
      <button type="button" class="btn btn-danger me-5" @click="signout">
        Signout
      </button>
      <div
        class="modal fade"
        id="staticBackdropList"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
        tabindex="-1"
        aria-labelledby="staticBackdropLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <form @submit="onSubmit">
              <div class="modal-header">
                <h1 class="modal-title fs-5" id="staticBackdropLabel">
                  Add List
                </h1>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <div class="mb-3">
                  <label for="cardTitle" class="form-label">List Title</label>
                  <input
                    type="text"
                    class="form-control"
                    name="title"
                    placeholder="title"
                    v-model="title"
                  />
                </div>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
                <button type="submit" class="btn btn-primary">Save</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
export default {
  name: "Navbar",
  props: {
    type: String,
  },
  data() {
    return {
      title: "",
    };
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      fetch("http://127.0.0.1:5000/addlist", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
        body: JSON.stringify({ title: this.title }),
      })
        .then((response) => response.json())
        .then((response) => {
          const res = response;
          if (!res.error) {
            const listRes = res.map(([id, userid, title]) => ({
              id,
              userid,
              title,
            }));
            this.$emit("add-title", listRes);
          } else {
            console.error(res.error);
          }
        });
      this.title = "";
    },
    signout() {
      localStorage.removeItem("jwt");
      this.$router.push("/");
      const triggerToast = document.getElementById("liveToast");
      document.getElementById("toast-text").innerHTML = "Signout Successful";
      const toast = new bootstrap.Toast(triggerToast);
      toast.show();
    },
  },
};
</script>
