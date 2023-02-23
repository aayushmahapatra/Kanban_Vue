<template>
  <main class="min-vh-100">
    <Navbar type="Export" />
    <section class="container p-5">
      <form
        enctype="multipart/form-data"
        class="card text-bg-dark border-light w-75 mb-5 mx-auto"
      >
        <div class="card-body">
          <h5 class="card-title fs-2">Import</h5>
          <p class="card-text">Import cards from csv.</p>
          <input
            type="file"
            @change="onFileChange"
            class="bg-light text-dark rounded-2"
          />
        </div>
      </form>
      <h2 class="text-light">Export</h2>
      <div class="card text-bg-dark border-light w-75 mb-3 mx-auto">
        <div class="card-body">
          <h5 class="card-title fs-2">Lists</h5>
          <p class="card-text">Export data of all lists in CSV format.</p>
          <button @click="formatLists(lists)" class="btn btn-primary">
            Export Lists as CSV
          </button>
        </div>
      </div>
      <div class="card text-bg-dark border-light w-75 mb-3 mx-auto">
        <div class="card-body">
          <h5 class="card-title fs-2">Cards</h5>
          <p class="card-text">Export data of all cards in CSV format.</p>
          <button @click="formatCards(cards)" class="btn btn-primary">
            Export Cards as CSV
          </button>
        </div>
      </div>
    </section>
  </main>
</template>

<script>
import Navbar from "@/components/Navbar.vue";

export default {
  name: "Export",
  components: {
    Navbar,
  },
  data() {
    return {
      lists: [],
      cards: [],
    };
  },
  created() {
    const jwt = localStorage.getItem("jwt");
    const jwtData = JSON.parse(atob(jwt.split(".")[1]));
    const expiry = jwtData.exp * 1000;
    const sessionExpired = new Date() < new Date(expiry);

    if (jwt && sessionExpired) {
      fetch(`http://127.0.0.1:5000/getdata`, {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
      })
        .then((response) => response.json())
        .then((response) => {
          const res = response;
          const listRes = res[0].map(([id, userid, title]) => ({
            id,
            userid,
            title,
          }));
          this.lists = listRes;
          const cardRes = res[1].map(
            ([
              id,
              userid,
              listid,
              list,
              title,
              content,
              deadline,
              completed,
              created_at,
              last_modified,
              completed_at,
            ]) => ({
              id,
              userid,
              listid,
              list,
              title,
              content,
              deadline,
              completed,
              created_at,
              last_modified,
              completed_at,
            })
          );
          this.cards = cardRes;
        });
    } else {
      this.$router.push("/");
    }
  },
  methods: {
    formatLists(lists) {
      const formattedList = [
        ["List ID", "List Title", "User ID"],
        ...lists.map((l) => [l.id, l.title, l.userid]),
      ];
      this.exportAsCsv(formattedList);
    },
    formatCards(cards) {
      const formattedCard = [
        [
          "Card ID",
          "User ID",
          "List ID",
          "List Title",
          "Card Title",
          "Card Content",
          "Card Deadline",
          "Card Completed",
          "Card Created At",
          "Last Modified",
          "Card Completed At",
        ],
        ...cards.map((c) => [
          c.id,
          c.userid,
          c.listid,
          c.list,
          c.title,
          c.content,
          new Date(c.deadline),
          c.completed,
          new Date(c.created_at),
          new Date(c.last_modified),
          c.completed_at ? new Date(c.completed_at) : null,
        ]),
      ];
      this.exportAsCsv(formattedCard);
    },
    exportAsCsv(formattedData) {
      let csvData =
        "data:text/csv;charset=utf-8," +
        formattedData.map((data) => data.join(",")).join("\n");
      console.log(csvData);

      // trigger download
      var dataURI = encodeURI(csvData);
      var downloadUrl = document.createElement("a");
      downloadUrl.setAttribute("href", dataURI);
      downloadUrl.setAttribute("download", "data.csv");
      document.body.appendChild(downloadUrl);
      downloadUrl.click();

      const triggerToast = document.getElementById("liveToast");
      document.getElementById("toast-text").innerHTML = "Export Successful";
      const toast = new bootstrap.Toast(triggerToast);
      toast.show();

      fetch(`http://127.0.0.1:5000/format_mail`, {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
      })
        .then((response) => response.json())
        .then((response) => {
          console.log(response);
        });
    },
    onFileChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      this.createImport(files[0]);
    },
    createImport(file) {
      let promise = new Promise((resolve) => {
        var reader = new FileReader();
        var vm = this;
        reader.onload = (e) => {
          resolve((vm.fileinput = reader.result));
        };
        reader.readAsText(file);
      });

      promise.then(
        (result) => {
          const formattedCsv = this.fileinput.split(/\r?\n/);
          const removeHeaders = formattedCsv.shift();
          const formattedValues = [];
          formattedCsv.map((c) => {
            let value = c.split(",");
            value[6] = new Date(value[6]).toLocaleString();
            value[8] = new Date(value[8]).toLocaleString();
            value[9] = new Date(value[9]).toLocaleString();
            value[10] = value[10] ? new Date(value[10]).toLocaleString() : "";
            formattedValues.push(value);
          });
          console.log(formattedValues);
          fetch("http://127.0.0.1:5000/importcsv", {
            method: "POST",
            headers: {
              Accept: "application/json",
              "Content-Type": "application/json",
              Authorization: "Bearer " + localStorage.getItem("jwt"),
            },
            body: JSON.stringify({
              csv: formattedValues,
            }),
          })
            .then((response) => response.json())
            .then((response) => {
              console.log(response);
              const triggerToast = document.getElementById("liveToast");
              document.getElementById("toast-text").innerHTML =
                "Import in progress";
              const toast = new bootstrap.Toast(triggerToast);
              toast.show();
            });
        },
        (error) => {
          console.log(error);
        }
      );
    },
  },
};
</script>

<style>
</style>

