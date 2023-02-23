<template>
  <main>
    <div
      class="modal fade"
      id="staticBackdrop2"
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
                Edit Card
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
                  v-model="editCard.title"
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
                  v-model="editCard.content"
                />
              </div>
              <div class="mb-3">
                <label for="deadline" class="form-label">Deadline</label>
                <input
                  type="datetime-local"
                  class="form-control"
                  name="deadline"
                  min="2022-12-25T14:06"
                  v-model="editCard.deadline"
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
  name: "EditCardModal",
  props: {
    editCard: Object,
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      fetch(`http://127.0.0.1:5000/editcard/${this.editCard.id}`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
        body: JSON.stringify({
          title: this.editCard.title,
          content: this.editCard.content,
          deadline: this.editCard.deadline,
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
          this.$emit("edit-card", cardRes);
        });
    },
  },
};
</script>
