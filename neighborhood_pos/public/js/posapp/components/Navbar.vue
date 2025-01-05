<template>
  <nav>
    <v-app-bar app height="48" class="elevation-0">
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
        class="grey--text"
      ></v-app-bar-nav-icon>
      <v-img
        src="/assets/neighborhood_pos/js/posapp/components/pos/logo.png"
        alt="POS"
        max-width="32"
        class="mr-2"
        color="primary"
      ></v-img>
      <v-toolbar-title
        @click="go_desk"
        style="cursor: pointer"
        class="text-uppercase primary--text"
      >
        <span class="font-weight-light">Neighborhood</span>
        <span>pos</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <v-btn style="cursor: unset" text color="primary">
        <span right>{{ pos_profile.name }}</span>
      </v-btn>
      <div class="text-center">
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary" dark text v-bind="attrs" v-on="on"
              >Menu</v-btn
            >
          </template>
          <v-card class="mx-auto" max-width="300" tile>
            <v-list dense>
              <v-list-item-group v-model="menu_item" color="primary">
                <v-list-item
                  @click="close_shift_dialog"
                  v-if="!pos_profile.posa_hide_closing_shift && item == 0"
                >
                  <v-list-item-icon>
                    <v-icon>mdi-content-save-move-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{
                      __("Close Shift")
                    }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item
                  @click="print_last_invoice"
                  v-if="
                    pos_profile.posa_allow_print_last_invoice &&
                    this.last_invoice
                  "
                >
                  <v-list-item-icon>
                    <v-icon>mdi-printer</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{
                      __("Print Last Invoice")
                    }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-divider class="my-0"></v-divider>
                <v-list-item @click="logOut">
                  <v-list-item-icon>
                    <v-icon>mdi-logout</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ __("Logout") }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item @click="go_about">
                  <v-list-item-icon>
                    <v-icon>mdi-information-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ __("About") }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-menu>
      </div>
    </v-app-bar>
    <v-navigation-drawer
      v-model="drawer"
      :mini-variant.sync="mini"
      app
      class=" margen-top"
      width="170"
      style="background: #0D1821;"
    >
      <v-list dark>
        <v-list-item class="px-2">
          <v-list-item-avatar>
            <v-img :src="company_img"></v-img>
          </v-list-item-avatar>

          <v-list-item-title>{{ company }}</v-list-item-title>

          <v-btn icon @click.stop="mini = !mini">
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item>
        <!-- <MyPopup/> -->
        <v-list-item-group v-model="item" color="white">
          <v-list-item
            v-for="item in items"
            :key="item.text"
            @click="changePage(item.text)"
          >
            <v-list-item-icon>
              <v-icon v-text="item.icon"></v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
    <!-- <v-snackbar v-model="snack" :timeout="5000" :color="snackColor" top right>
      {{ snackText }}
    </v-snackbar> -->
    <div>
      <v-snackbar
        v-model="snack"
        top
        right
        :elevation="0"
        :timeout="5000"
        :color="snackColor"
        class="snack"
        :class="'snack-type-' + type"
      >
        <div class="notification-content">
          <div class="notification-icon" :class="type">
            <!-- <i class="fa fa-check-circle" v-if="type == 'success'" ></i> -->
            <v-icon v-if="type == 'success'">mdi-check-bold</v-icon>
            <v-icon v-if="type == 'error'">mdi-alert-circle</v-icon>
            <!-- <i class="fa fa-exclamation-triangle" v-if="type == 'error' || type == 'warning'" ></i> -->
            <i class="fa fa-info-circle" v-if="type == 'info'"></i>
          </div>

          <div class="notification-message">
            {{ snackText }}
          </div>
        </div>
        <template v-slot:action="{ attrs }">
          <a class="close-notification-button" v-bind="attrs">
            <i class="fa fa-times"></i>
          </a>
        </template>
      </v-snackbar>
    </div>
    <v-dialog v-model="freeze" persistent max-width="290">
      <v-card>
        <v-card-title class="text-h5">
          {{ freezeTitle }}
        </v-card-title>
        <v-card-text>{{ freezeMsg }}</v-card-text>
      </v-card>
    </v-dialog>
  </nav>
</template>

<script>
import { evntBus } from "../bus";

export default {
  // components: {MyPopup},
  data() {
    return {
      drawer: false,
      mini: true,
      item: 0,
      items: [{ text: "POS", icon: "mdi-network-pos" }],
      page: "",
      fav: true,
      menu: false,
      message: false,
      hints: true,
      menu_item: 0,
      snack: false,
      snackColor: "",
      snackText: "",
      company: "POS",
      company_img: "/assets/neighborhood_pos/js/posapp/components/pos/logo.png",
      pos_profile: "",
      freeze: false,
      freezeTitle: "",
      freezeMsg: "",
      last_invoice: "",
      type: "info",
    };
  },
  methods: {
    changePage(key) {
      this.$emit("changePage", key);
    },
    go_desk() {
      frappe.set_route("/");
      location.reload();
    },
    go_about() {
      const win = window.open("https://zajel.com", "_blank");
      win.focus();
    },
    close_shift_dialog() {
      evntBus.$emit("open_closing_dialog");
    },
    show_mesage(data) {
      this.snack = true;
      this.snackColor = data.color;
      this.snackText = data.text;
      this.type = data.color;
    },
    logOut() {
      var me = this;
      me.logged_out = true;
      return frappe.call({
        method: "logout",
        callback: function (r) {
          if (r.exc) {
            return;
          }
          frappe.set_route("/login");
          location.reload();
        },
      });
    },
    print_last_invoice() {
      if (!this.last_invoice) return;
      const print_format =
        this.pos_profile.print_format_for_online ||
        this.pos_profile.print_format;
      const letter_head = this.pos_profile.letter_head || 0;
      const url =
        frappe.urllib.get_base_url() +
        "/printview?doctype=Sales%20Invoice&name=" +
        this.last_invoice +
        "&trigger_print=1" +
        "&format=" +
        "Sales%20Invoice%20Print" +
        "&no_letterhead=" +
        letter_head;
      const printWindow = window.open(url, "Print");
      printWindow.addEventListener(
        "load",
        function () {
          printWindow.print();
        },
        true
      );
    },
  },
  created: function () {
    this.$nextTick(function () {
      evntBus.$on("show_mesage", (data) => {
        this.show_mesage(data);
      });
      evntBus.$on("set_company", (data) => {
        this.company = data.name;
        this.company_img = data.company_logo
          ? data.company_logo
          : this.company_img;
      });
      evntBus.$on("register_pos_profile", (data) => {
        this.pos_profile = data.pos_profile;
        const payments = { text: "Payments", icon: "mdi-cash-register" };
        if (
          this.pos_profile.posa_use_pos_awesome_payments &&
          this.items.length !== 2
        ) {
          this.items.push(payments);
        }
      });
      evntBus.$on("set_last_invoice", (data) => {
        this.last_invoice = data;
      });
      evntBus.$on("freeze", (data) => {
        this.freeze = true;
        this.freezeTitle = data.title;
        this.freezeMsg = data.msg;
      });
      evntBus.$on("unfreeze", () => {
        this.freeze = false;
        this.freezTitle = "";
        this.freezeMsg = "";
      });
    });
  },
};
</script>

<style scoped>
.margen-top {
  margin-top: 0px;
}
</style>
<style>
.notification-content {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.notification-content .notification-icon.success {
  background-color: #3fbf62;
}
.notification-content .notification-icon.error {
  background-color: #ec4f2b;
}
.notification-content .notification-icon.info {
  background-color: #016de6;
}
.notification-content .notification-icon.warning {
  background-color: #ee9401;
}

.v-snack.snack-type-success .v-snack__wrapper {
  background-color: #eaf7ee !important;
  border: 1px solid #a4ddb4 !important;
}
.v-snack.snack-type-error .v-snack__wrapper {
  background-color: #fcece9 !important;
  border: 1px solid #f4c5bb !important;
}
.v-snack.snack-type-info .v-snack__wrapper {
  background-color: #e4effa !important;
  border: 1px solid #abcdf1 !important;
}
.v-snack.snack-type-warning .v-snack__wrapper {
  background-color: #fef7e9 !important;
  border: 1px solid #fde0af !important;
}
.notification-content .notification-message {
  color: #484848 !important;
}
.notification-content .notification-icon i {
  width: 27px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.notification-content .notification-icon {
  font-size: 25px !important;
  padding: 5px;
  border-radius: 8px;
  margin-right: 10px;
}

.v-snack__btn.close-notification-button {
  color: #484848;
  margin-right: 10px;
}

.v-snack__content {
  padding: 5px 7px !important;
}
</style>