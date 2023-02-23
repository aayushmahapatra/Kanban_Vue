<template>
  <main>
    <div
      class="modal fade"
      id="staticBackdrop"
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
                Add Card
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
                <label for="cardTitle" class="form-label">Card Title</label>
                <input
                  type="text"
                  class="form-control"
                  name="title"
                  v-model="cardTitle"
                />
              </div>
              <div class="mb-3">
                <label for="cardContent" class="form-label">
                  Card Content
                </label>
                <input
                  type="text"
                  class="form-control"
                  name="content"
                  v-model="cardContent"
                />
              </div>
              <div class="mb-3">
                <label for="deadline" class="form-label">Deadline</label>
                <input
                  type="datetime-local"
                  class="form-control"
                  name="deadline"
                  min="2022-12-25T14:06"
                  v-model="deadline"
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
  </main>
</template>

<script>
export default {
  name: "AddCardModal",
  props: {
    lists: Array,
    listId: Number,
    cards: Array,
  },
  data() {
    return {
      cardTitle: "",
      cardContent: "",
      deadline: "",
    };
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      const listIndex = this.lists.findIndex((l) => l.id === this.listId);
      fetch("http://127.0.0.1:5000/addcard", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
        body: JSON.stringify({
          listid: this.listId,
          list: this.lists[listIndex].title,
          title: this.cardTitle,
          content: this.cardContent,
          deadline: this.deadline,
        }),
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
          this.$emit("add-card", cardRes);
        });
      this.cardTitle = "";
      this.cardContent = "";
      this.deadline = "";
    },
  },
};
</script>
