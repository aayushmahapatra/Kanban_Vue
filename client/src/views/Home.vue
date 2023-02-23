<template>
  <main class="min-vh-100 p-5">
    <div>
      <button
        @click="signup = false"
        :class="{ active: !signup }"
        class="btn btn-light fw-semibold me-3"
      >
        Signin
      </button>
      <button
        @click="signup = true"
        :class="{ active: signup }"
        class="btn btn-light fw-semibold"
      >
        Signup
      </button>
    </div>
    <section
      v-if="signup === false"
      class="d-flex justify-content-center align-items-center"
    >
      <form
        class="container bg-light w-25 m-5 p-4 rounded box"
        @submit="onSignin"
      >
        <h3 class="fw-bold">KANBAN</h3>
        <div class="mb-3">
          <label for="email" class="form-label label text-start">Email</label>
          <input
            type="text"
            class="form-control"
            name="email"
            placeholder="email"
            v-model="email"
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label label text-start"
            >Password</label
          >
          <input
            type="password"
            class="form-control"
            name="password"
            placeholder="password"
            v-model="password"
          />
        </div>
        <button type="submit" class="btn btn-success">Signin</button>
      </form>
    </section>
    <section v-else class="d-flex justify-content-center align-items-center">
      <form
        class="container bg-light w-25 m-5 p-4 rounded box"
        @submit="onSignup"
      >
        <h3 class="fw-bold">KANBAN</h3>
        <div class="mb-3">
          <label for="name" class="form-label label text-start">Name</label>
          <input
            type="text"
            class="form-control"
            name="name"
            placeholder="name"
            v-model="name"
          />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label label text-start">Email</label>
          <input
            type="text"
            class="form-control"
            name="email"
            placeholder="email"
            v-model="email"
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label label text-start"
            >Password</label
          >
          <input
            type="password"
            class="form-control"
            name="password"
            placeholder="password"
            v-model="password"
          />
        </div>
        <div class="mb-3">
          <label for="confirm_password" class="form-label label text-start"
            >Confirm Password</label
          >
          <input
            type="password"
            class="form-control"
            name="confirm_password"
            placeholder="confirm password"
            v-model="confirm_password"
          />
        </div>
        <button type="submit" class="btn btn-success">Signup</button>
      </form>
    </section>
  </main>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      signup: false,
      name: "",
      email: "",
      password: "",
      confirm_password: "",
    };
  },
  methods: {
    async onSignin(e) {
      e.preventDefault();
      fetch("http://127.0.0.1:5000/signin", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: this.email, password: this.password }),
      })
        .then((response) => response.json())
        .then((response) => {
          const res = JSON.parse(JSON.stringify(response));
          if (res !== "Login Failed") {
            localStorage.setItem("jwt", res.token);
            this.email = "";
            this.$router.push("dashboard");
            const triggerToast = document.getElementById("liveToast");
            document.getElementById("toast-text").innerHTML =
              "Signin Successful";
            const toast = new bootstrap.Toast(triggerToast);
            toast.show();
          }
          this.password = "";
        });
    },
    async onSignup(e) {
      e.preventDefault();
      fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: this.name,
          email: this.email,
          password: this.password,
          confirm_password: this.confirm_password,
        }),
      })
        .then((response) => response.json())
        .then((response) => {
          if (response == "Success") {
            this.name = "";
            this.email = "";
            this.password = "";
            this.confirm_password = "";
            this.signup = false;
          }
        });
    },
  },
};
</script>

<style scoped>
.label {
  font-size: 12px;
}
.active {
  background: #6ac47e;
  box-shadow: 0 15px 15px #101214;
}
.box {
  box-shadow: 10px 15px 15px #101214;
}
</style>
