// registrationStore.js
import { defineStore } from "pinia";
import { ref } from "vue";

export const useRegistrationStore = defineStore("cartStore", () => {
  const activeUser = ref("Guest");
  const isSignedIn = ref(false);
  const isAdmin = ref(false);

  const userInfo = ref({})

    //TODO: fetch and see if the user exists at all
  async function activateUser(username) {
    if (username === "admin") {
      isAdmin.value = true;
    }
    activeUser.value = username;
    isSignedIn.value = true;
  }

  function deactivateUser() {
    activeUser.value = "Guest";
    isSignedIn.value = false;
  }

  return {
    activeUser,
    isSignedIn,
    activateUser,
    deactivateUser,
  };
});
