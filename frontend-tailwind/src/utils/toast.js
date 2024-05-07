import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const notifySuccess = (message) => {
  toast(message, {
    type: "success",
    dangerouslyHTMLString: true,
    pauseOnFocusLoss: false,
  });
};

const notifyFail = (message) => {
  toast(message, {
    type: "error",
    dangerouslyHTMLString: true,
    pauseOnFocusLoss: false,
  });
};

export { notifySuccess, notifyFail };
