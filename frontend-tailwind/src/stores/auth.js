import { defineStore } from "pinia";
import { ref } from "vue";
import { notifySuccess, notifyFail } from "@/utils/toast.js";

export const useAuthStore = defineStore("auth", () => {
  const isLoginPopupOpen = ref(false);
  const isRegisterPopupOpen = ref(false);
  const profileData = ref({ full_name: "Guest" });
  const isLoggedIn = ref(false);

  function setLoginPopupOpenStatus(status) {
    isLoginPopupOpen.value = status;
  }

  function setRegisterPopupOpenStatus(status) {
    isRegisterPopupOpen.value = status;
  }

  async function signUp(payload) {
    try {
      const res = await httpClient.post("/auth/signup", {
        ...payload,
      });
      notifySuccess(res.data.message);
      setRegisterPopupOpenStatus(false);
      setLoginPopupOpenStatus(true);
    } catch (e) {
      notifyFail(e.message);
    }
  }

  async function signIn(payload) {
    try {
      const res = await httpClient.post("/auth/signin", {
        ...payload,
      });
      localStorage.setItem(AUTH_TOKEN_KEY, res.data.access_token);
      notifySuccess(res.data.message);
      setLoginPopupOpenStatus(false);
      isLoggedIn.value = true;
    } catch (e) {
      notifyFail(e.message);
      isLoggedIn.value = false;
    }
  }

  function signOut() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    isLoggedIn.value = false;
    profileData.value = null;
  }

  return {
    isLoginPopupOpen,
    isRegisterPopupOpen,
    profileData,
    isLoggedIn,
    setLoginPopupOpenStatus,
    setRegisterPopupOpenStatus,
    signUp,
    signIn,
    signOut,
  };
});
