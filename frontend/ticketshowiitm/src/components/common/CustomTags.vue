<template>
  <div :class="tagsClass">
    <div v-if="tagString">
      <span v-for="tag in tagsArray" :key="tag" class="tag">{{ tag }}</span>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tagString: {
      type: String,
      required: true,
    },
    left: {
      type: Boolean,
      default: true,
    },
    center: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    tagsArray() {
      // Split the tagString into an array using the ',' separator
      // If tagString is not defined or is null, return an empty array
      return this.tagString ? this.tagString.split(",") : [];
    },
    tagsClass() {
      return {
        "left": this.left && !this.center,
        "center": this.center,
      };
    },
  },
};
</script>

<style scoped>
.custom-tags {
  display: flex;
  flex-wrap: wrap;
}

.tag {
  background-color: #f0f0f0;
  color: #7c7b7b;
  border-radius: 10px;
  padding: 5px 10px;
  margin: 5px;
  font-size: 14px;
}

.left {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
}

.center {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

</style>
