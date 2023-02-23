<template>
  <main class="min-vh-100">
    <Navbar type="Export" />
    <section class="container p-5">
      <section class="row">
        <div class="col-4 px-3">
          <div class="card text-bg-light py-3">
            <h5 class="card-title fs-2">Total Tasks</h5>
            <span class="fs-1 fw-bold">{{ total_tasks }}</span>
          </div>
        </div>
        <div class="col-4 px-3">
          <div class="card text-bg-light py-3">
            <h5 class="card-title fs-2">Total Completed</h5>
            <span class="fs-1 fw-bold">{{ total_completed }}</span>
          </div>
        </div>
        <div class="col-4 px-3">
          <div class="card text-bg-light py-3">
            <h5 class="card-title fs-2">Total Missed</h5>
            <span class="fs-1 fw-bold">{{ total_missed }}</span>
          </div>
        </div>
      </section>
      <div
        id="chart"
        class="d-flex justify-content-center mt-4 bg-light rounded-2 py-3"
      >
        <apexchart
          width="800"
          type="bar"
          :options="options"
          :series="series"
        ></apexchart>
      </div>
    </section>
  </main>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import Navbar from "@/components/Navbar.vue";

export default {
  name: "Export",
  components: {
    Navbar,
    apexchart: VueApexCharts,
  },
  data() {
    return {
      total_tasks: 0,
      total_completed: 0,
      total_missed: 0,
      options: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          categories: [],
        },
        title: {
          text: "Tasks by Date: Total vs Completed vs Missed",
          align: "center",
          style: {
            fontSize: "20px",
          },
        },
      },
      series: [],
    };
  },
  created() {
    const jwt = localStorage.getItem("jwt");
    const jwtData = JSON.parse(atob(jwt.split(".")[1]));
    const expiry = jwtData.exp * 1000;
    const sessionExpired = new Date() < new Date(expiry);

    if (jwt && sessionExpired) {
      fetch(`http://127.0.0.1:5000/stats`, {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
      })
        .then((response) => response.json())
        .then((response) => {
          this.total_tasks = response[0];
          this.total_completed = response[1];
          this.total_missed = response[2];
          let categories = [];
          Object.keys(response[3]).map((key) => categories.push(key));
          this.options = {
            chart: { id: "tasks" },
            xaxis: { categories },
          };
          // total tasks
          let tasks = [];
          Object.values(response[3]).map((value) => tasks.push(value));
          this.series = [
            {
              name: "total-tasks",
              data: tasks,
            },
          ];
          // total completed
          let completed = [];
          Object.values(response[4]).map((value) => completed.push(value));
          this.series = [
            ...this.series,
            {
              name: "total-completed",
              data: completed,
            },
          ];
          // total missed
          let missed = [];
          Object.values(response[5]).map((value) => missed.push(value));
          this.series = [
            ...this.series,
            {
              name: "total-missed",
              data: missed,
            },
          ];
        });
    } else {
      this.$router.push("/");
    }
  },
  methods: {},
};
</script>

<style>
</style>

