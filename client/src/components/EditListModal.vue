<template>
  <main>
    <div
      class="modal fade"
      id="staticBackdropList2"
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
                Edit List
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
                  v-model="editList.title"
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
  name: "EditListModal",
  props: {
    editList: Object,
  },
  methods: {
    onSubmit(e) {
      e.preventDefault();
      fetch(`http://127.0.0.1:5000/editlist/${this.editList.id}`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: "Bearer " + localStorage.getItem("jwt"),
        },
        body: JSON.stringify({ title: this.editList.title }),
      })
        .then((response) => response.json())
        .then((response) => {
          const res = response;
          const listRes = res.map(([id, userid, title]) => ({
            id,
            userid,
            title,
          }));
          this.$emit("edit-list", listRes);
        });
    },
  },
};
</script>
