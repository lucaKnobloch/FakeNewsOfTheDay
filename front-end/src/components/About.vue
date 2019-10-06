<template>
  <div>
    <h1>About</h1>
    <p>{{ msg }}</p>
  </div>
</template>

<script>

export default {
  name: 'About', //this is the name of the component
   data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://localhost:5000/about';
      axios.get(path)
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
}
</script>
<style>
</style>