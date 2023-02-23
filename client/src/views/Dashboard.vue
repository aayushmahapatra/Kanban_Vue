<template>
  <main class="min-vh-100">
    <Navbar type="Dashboard" @add-title="onListSubmit" />
    <section class="container">
      <section class="row">
        <section
          v-for="(list, listIndex) in lists"
          :key="listIndex"
          class="card text-bg-dark border-light m-3 col-3 box"
          style="max-width: 18rem"
        >
          <div class="card-header border-light d-flex justify-content-between">
            <h2>{{ list.title }}</h2>
            <div>
              <button
                type="button"
                class="btn p-0"
                data-bs-toggle="modal"
                data-bs-target="#staticBackdrop"
                @click="onAdd(list.id)"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 16 16"
                  width="20"
                  height="20"
                  id="svg"
                >
                  <path
                    d="M2.75 1h10.5c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0 1 13.25 15H2.75A1.75 1.75 0 0 1 1 13.25V2.75C1 1.784 1.784 1 2.75 1Zm10.5 1.5H2.75a.25.25 0 0 0-.25.25v10.5c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25V2.75a.25.25 0 0 0-.25-.25ZM8 4a.75.75 0 0 1 .75.75v2.5h2.5a.75.75 0 0 1 0 1.5h-2.5v2.5a.75.75 0 0 1-1.5 0v-2.5h-2.5a.75.75 0 0 1 0-1.5h2.5v-2.5A.75.75 0 0 1 8 4Z"
                  ></path>
                </svg>
              </button>
              <button
                type="button"
                class="btn"
                data-bs-toggle="modal"
                data-bs-target="#staticBackdropList2"
                @click="openEditList(list.id)"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 16 16"
                  width="20"
                  height="20"
                  id="svg"
                >
                  <path
                    d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064Zm1.238-3.763a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354Z"
                  ></path>
                </svg>
              </button>
              <button class="btn p-0" @click="onDeleteList(list.id)">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 16 16"
                  width="20"
                  height="20"
                  id="svg"
                >
                  <path
                    d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"
                  ></path>
                </svg>
              </button>
            </div>
          </div>
          <div class="card-body">
            <div v-for="(card, cardIndex) in cards" :key="cardIndex">
              <div
                v-if="card.listid === list.id"
                class="card text-bg-light mb-3"
                style="max-width: 18rem"
              >
                <div
                  class="
                    card-header
                    d-flex
                    justify-content-between
                    align-items-center
                  "
                >
                  <h4 class="m-0">{{ card.title }}</h4>
                  <div>
                    <button
                      type="button"
                      class="btn"
                      data-bs-toggle="modal"
                      data-bs-target="#staticBackdrop2"
                      @click="openEditCard(card.id)"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 16 16"
                        width="20"
                        height="20"
                      >
                        <path
                          d="M11.013 1.427a1.75 1.75 0 0 1 2.474 0l1.086 1.086a1.75 1.75 0 0 1 0 2.474l-8.61 8.61c-.21.21-.47.364-.756.445l-3.251.93a.75.75 0 0 1-.927-.928l.929-3.25c.081-.286.235-.547.445-.758l8.61-8.61Zm.176 4.823L9.75 4.81l-6.286 6.287a.253.253 0 0 0-.064.108l-.558 1.953 1.953-.558a.253.253 0 0 0 .108-.064Zm1.238-3.763a.25.25 0 0 0-.354 0L10.811 3.75l1.439 1.44 1.263-1.263a.25.25 0 0 0 0-.354Z"
                        ></path>
                      </svg>
                    </button>
                    <button
                      class="border border-0"
                      @click="onDeleteCard(card.id)"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 16 16"
                        width="20"
                        height="20"
                      >
                        <path
                          d="M11 1.75V3h2.25a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5H5V1.75C5 .784 5.784 0 6.75 0h2.5C10.216 0 11 .784 11 1.75ZM4.496 6.675l.66 6.6a.25.25 0 0 0 .249.225h5.19a.25.25 0 0 0 .249-.225l.66-6.6a.75.75 0 0 1 1.492.149l-.66 6.6A1.748 1.748 0 0 1 10.595 15h-5.19a1.75 1.75 0 0 1-1.741-1.575l-.66-6.6a.75.75 0 1 1 1.492-.15ZM6.5 1.75V3h3V1.75a.25.25 0 0 0-.25-.25h-2.5a.25.25 0 0 0-.25.25Z"
                        ></path>
                      </svg>
                    </button>
                  </div>
                </div>
                <div class="card-body">
                  <p class="card-text">{{ card.content }}</p>
                </div>
                <select
                  class="m-2"
                  v-model="card.listid"
                  @change="onMove(card.listid, card.id)"
                >
                  <option
                    v-for="(list, index) in lists"
                    :key="index"
                    :value="list.id"
                  >
                    {{ list.title }}
                  </option>
                </select>
                <div class="card-footer small-font">
                  <p
                    class="m-0 mb-1"
                    :class="{ missed: new Date() > new Date(card.deadline) }"
                  >
                    {{ new Date(card.deadline).toLocaleDateString("en-IN") }}
                    -
                    {{ new Date(card.deadline).toLocaleTimeString("en-IN") }}
                  </p>
                  <div
                    :class="{ completed: card.completed }"
                    class="d-flex justify-content-center align-items-center"
                  >
                    <input
                      type="checkbox"
                      id="completed"
                      name="vehicle1"
                      v-model="card.completed"
                      @change="handleCompleted(card.completed, card.id)"
                      class="me-2"
                    />
                    <label for="completed">Complete</label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </section>
    </section>
    <EditListModal :editList="editList" @edit-list="onEditList" />
    <AddCardModal
      :lists="lists"
      :listId="listId"
      :cards="cards"
      @add-card="onAddCard"
    />
    <EditCardModal :editCard="editCard" @edit-card="onEditCard" />
  </main>
</template>

<script>
import EditListModal from "@/components/EditListModal.vue";
import AddCardModal from "@/components/AddCardModal.vue";
import EditCardModal from "@/components/EditCardModal.vue";
import Navbar from "@/components/Navbar.vue";

export default {
  name: "Dashboard",
  components: {
    EditListModal,
    AddCardModal,
    EditCardModal,
    Navbar,
  },
  data() {
    return {
      lists: [],
      cards: [],
      listId: null,
      editList: {},
      editCard: {},
    };
  },
  created() {
    const jwt = localStorage.getItem("jwt");
    let sessionExpired;
    if (jwt) {
      const jwtData = JSON.parse(atob(jwt.split(".")[1]));
      const expiry = jwtData.exp * 1000;
      sessionExpired = new Date() < new Date(expiry);
    }
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
            })
          );
          this.cards = cardRes;
        });
    } else {
      this.$router.push("/");
    }
  },
  methods: {
    onListSubmit(lists) {
      this.lists = lists;
    },
    onAdd(listId) {
      this.listId = listId;
    },
    openEditList(listId) {
      this.editList = this.lists.filter((l) => l.id === listId)[0];
    },
    onEditList(lists) {
      this.lists = lists;
    },
    onDeleteList(listId) {
      let warning = "Are you sure you want to delete the entire list?";
      if (confirm(warning) == true) {
        fetch(`http://127.0.0.1:5000/deletelist/${listId}`, {
          method: "DELETE",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("jwt"),
          },
        })
          .then((response) => response.json())
          .then((response) => {
            const res = response;
            const listRes = res.map(([id, userid, title]) => ({
              id,
              userid,
              title,
            }));
            this.lists = listRes;
          });
      }
    },
    onAddCard(cards) {
      this.cards = cards;
    },
    openEditCard(cardId) {
      this.editCard = this.cards.filter((c) => c.id === cardId)[0];
      const date = new Date(this.editCard.deadline);
      const dateStr =
        date.getFullYear() +
        "-" +
        ("00" + (date.getMonth() + 1)).slice(-2) +
        "-" +
        ("00" + date.getDate()).slice(-2) +
        "T" +
        ("00" + date.getHours()).slice(-2) +
        ":" +
        ("00" + date.getMinutes()).slice(-2) +
        ":" +
        ("00" + date.getSeconds()).slice(-2);
      this.editCard.deadline = dateStr;
    },
    onEditCard(cards) {
      this.cards = cards;
    },
    onMove(listid, cardId) {
      const list = this.cards.filter((c) => c.id === cardId)[0].list;
      fetch(`http://127.0.0.1:5000/movecard/${cardId}`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
        body: JSON.stringify({ listid, list }),
      })
        .then((response) => response.json())
        .then((response) => {
          const res = response;
          const cardRes = res.map(
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
            })
          );
          this.cards = cardRes;
        });
    },
    handleCompleted(completed, cardId) {
      fetch(`http://127.0.0.1:5000/completed/${cardId}`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
        body: JSON.stringify({ completed }),
      })
        .then((response) => response.json())
        .then((response) => {
          const res = response;
          const cardRes = res.map(
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
            })
          );
          this.cards = cardRes;
        });
    },
    onDeleteCard(cardId) {
      let warning = "Are you sure you want to delete the card?";
      if (confirm(warning) == true) {
        fetch(`http://127.0.0.1:5000/deletecard/${cardId}`, {
          method: "DELETE",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("jwt"),
          },
        })
          .then((response) => response.json())
          .then((response) => {
            const res = response;
            const cardRes = res.map(
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
              })
            );
            this.cards = cardRes;
          });
      }
    },
  },
};
</script>

<style>
#svg {
  fill: white;
}
.small-font {
  font-size: 14px;
}
.completed {
  background: #6ac47e;
  border-radius: 5px;
}
.missed {
  background: #de4839;
  color: white;
  border-radius: 5px;
}
.box {
  box-shadow: 20px 20px 35px #141719;
}
</style>

