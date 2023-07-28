<template>
  <div class="create-show">
    <CustomHeading1 class="heading">Create Show</CustomHeading1>
    <form @submit.prevent="submitForm">
      <CustomInputText
        label="Name"
        type="text"
        placeholder="Enter show name"
        :value="name"
        required="true"
        @update:value="name = $event"
      />
      <CustomInputText
        label="Rating"
        type="number"
        placeholder="Enter show rating"
        :value="rating"
        required="true"
        @update:value="rating = $event"
      />
      <CustomInputText
        label="Tags"
        type="string"
        placeholder="Enter show tags separated by comma"
        :value="tags"
        required="true"
        @update:value="tags = $event"
      />
      <CustomInputText
        label="Ticket Price"
        type="number"
        placeholder="Enter ticket price of the show"
        :value="ticketPrice"
        required="true"
        @update:value="ticketPrice = $event"
      />
      <div class="btn">
      <CustomAppButton type="submit">Create</CustomAppButton>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import CustomHeading1 from "../../common/CustomHeading1.vue";
import CustomInputText from "../../common/CustomTextInput.vue";
import CustomAppButton from "../../common/CustomAppButton.vue";

export default {
  name: "CreateShow",
  data() {
    return {
      name: "",
      rating: "",
      tags: "",
      ticketPrice: null,
    };
  },
  components: {
    CustomHeading1,
    CustomInputText,
    CustomAppButton,
  },
  methods: {
    submitForm() {
      const theatreId = this.$route.params.id;
      console.log(theatreId);
      const newShow = {
        name: this.name,
        rating: this.rating,
        tags: this.tags,
        ticket_price: this.ticketPrice,
        theatre_id: theatreId,
      };
      console.log(newShow);
      // Make API call to create a new show
      axios.post("http://localhost:5000/api/shows", newShow)
        .then((response) => {
          console.log("Show created successfully:", response.data);
          // Redirect to the ShowList page after successful creation
          this.$router.push("/AdminHome");
        })
        .catch((error) => {
          console.error("Error creating show:", error);
        });
    },
  },
};
</script>

<style>
.create-show {
  display: block;
  padding: 10% 20%;
}

.heading {
  text-align: center;
}

.btn {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}
</style>
