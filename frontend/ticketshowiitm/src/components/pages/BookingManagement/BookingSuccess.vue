<template>
    <div class="full-page">
        <i class="fa-solid fa-face-laugh fa-2xl" style="color: #ff5252;"></i>
        <h1>Booking Success</h1>
        <CustomAppButton @click="goToHome">Go to Home</CustomAppButton>
    </div>
</template>
<script>
import CustomAppButton from '@/components/common/CustomAppButton.vue';

export default{
    components:{
        CustomAppButton
    },
    methods:{
        goToHome(){
            this.$router.push('/clienthome')
        }
    }
}

</script>

<style scoped>
.full-page{
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

</style>