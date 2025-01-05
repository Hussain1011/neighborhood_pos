<template>
  <v-row justify="center">
    <v-dialog
      v-model="varaintsDialog"
      width="600"
      max-height="800px"
      persistent
    >
      <v-card class="dialog-main" v-if="parentItem">
        <v-card-title class="text-h5 d-flex justify-end pt-3 pr-3">
          <v-icon
            class="d-flex justify-end pt-3 pr-3"
            @click="close_dialog"
            :ripple="false"
          >
            mdi-close
          </v-icon>
        </v-card-title>
        <v-card-title class="text-h5 d-flex justify-center pt-7 px-10 pb-0">
          <p class="title-p">Select Your Item</p>


          <!-- <v-spacer></v-spacer>
             <v-icon> mdi-close </v-icon> -->
        </v-card-title>
        <p class="d-flex justify-center parent-p">
          {{ parentItem.item_name }}
        </p>

        <v-card-text class="pt-4 pb-0 add-on-div">
          <div v-if="parentItem.attributes">
            <v-expansion-panels
              class="mb-6"
              style="z-index: auto"
              multiple
              v-model="panel"
            >
              <v-expansion-panel
                v-for="(item, i) in parentItem.attributes"
                :key="i"
                class=""
              >
                <v-expansion-panel-header class="header-font panel-item">
                  {{ item.attribute }}
                  <template v-slot:actions>
                    <p
                      v-if="item.required && !item.valueSelect"
                      class="required-p"
                    >
                      Required
                    </p>
                    <div v-if="item.valueSelect" class="py-0">
                      <p class="added-p">Added</p>
                    </div>
                    <v-icon color="#718096">
                      {{ panel.includes(i) ? "mdi-chevron-up" : "mdi-plus" }}
                    </v-icon>
                  </template>
                </v-expansion-panel-header>
                <v-expansion-panel-content
                  v-if="item.values.length > 0"
                  class="px-0 pt-1 context-bg"
                >
                  <div
                    v-for="(option, index) in item.values"
                    :key="index"
                    class="d-flex justify-space-between radio-div"
                  >
                    <v-radio-group
                      v-model="variantRadio[i]"
                      class="py-0"
                      @change="onRadioChange(i, $event)"
                    >
                      <v-radio
                        :value="option"
                        class="mr-1 radio-button"
                        :ripple="false"
                      >
                        <template v-slot:label>
                          <div class="mt-2">
                            {{ option.abbr }}
                          </div>
                        </template>
                      </v-radio>
                    </v-radio-group>
                    <!-- </div> -->
                    <!-- <div class="mt-4">
                      <span>Rs. {{ option.rate }}</span>
                    </div> -->
                  </div>
                </v-expansion-panel-content>
                <v-expansion-panel-content
                  v-else-if="
                    item.title == 'Add a Drink' ||
                    'Add Extra' ||
                    'Add Apeteasers'
                  "
                  class="px-0 pt-1 context-bg"
                >
                  <div
                    v-for="(option, index) in getOptionsArray(item.title)"
                    :key="index"
                    class="d-flex justify-space-between radio-div"
                  >
                    <div>
                      <v-checkbox
                        :label="option.label"
                        :value="option.value"
                        :model-value="getSelectedModel(item.title)"
                        @change="
                          updateSelectedModel($event, item.title, index, i)
                        "
                        class="mr-3 radio-button"
                      ></v-checkbox>
                    </div>
                    <div class="mt-4">
                      <span>Rs.{{ option.price }}</span>
                    </div>
                  </div>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </v-card-text>

        <!-- add on items -->
        <v-card-text class="pt-0 add-on-content">
          <div v-if="parentItem.add_ons">
            <v-expansion-panels
              class="mb-6"
              style="z-index: auto"
              multiple
              v-model="addOnpanel"
            >
              <v-expansion-panel
                v-for="(item, i) in parentItem.add_ons"
                :key="i"
                class=""
              >
                <!-- <div v-if="!item.hide"> -->
                <v-expansion-panel-header class="header-font panel-item">
                  {{ item.display_name }}
                  <template v-slot:actions>
                    <!-- <p

                      v-if="item.required && !item.valueSelect"
                      class="required-p"
                    >
                      Required
                    </p>
                    <div v-if="item.valueSelect" class="py-0">
                      <p class="added-p">Added</p>
                    </div> -->

                    <v-icon color="#718096">
                      {{
                        addOnpanel.includes(i) ? "mdi-chevron-up" : "mdi-plus"
                      }}
                    </v-icon>
                  </template>
                </v-expansion-panel-header>
                <!-- <v-expansion-panel-content
                  v-if="item.item_add_ons.length > 0"
                  class="px-0 pt-1 context-bg"
                >
                  <div
                    v-for="(option, index) in item.item_add_ons"
                    :key="index"
                    class="d-flex justify-space-between radio-div"
                  >
                    <v-radio-group
                      v-model="selectedValues[i]"
                      class="py-0"
                      @change="addOnChange(i, $event)"
                    >
                      <v-radio
                        :value="option"
                        class="mr-1 radio-button"
                        :ripple="false"
                      >
                        <template v-slot:label>
                          <div class="mt-2">{{ option.display_name }}</div>
                        </template>
                      </v-radio>
                    </v-radio-group>
                    <div class="mt-4">
                      <span>Rs. {{ option.rate }}</span>
                    </div>
                  </div>
                </v-expansion-panel-content> -->
                <v-expansion-panel-content
                  v-if="item.item_add_ons.length > 0"
                  class="px-0 pt-1 context-bg"
                >
                  <div
                    v-for="(option, index) in item.item_add_ons"
                    :key="index"
                    class="d-flex justify-space-between radio-div"
                  >
                    <div>
                      <v-checkbox
                        :value="option"
                        v-model="selectedValues[i]"
                        class="mr-3 radio-button"
                        multiple
                      >
                        <template v-slot:label>
                          <div class="mt-2">{{ option.display_name }}</div>
                        </template>
                      </v-checkbox>
                    </div>
                    <div class="mt-4">
                      <span>Rs.{{ option.rate || 0 }}</span>
                    </div>
                  </div>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </v-card-text>
        <!-- <v-card-text>
          <div class="d-flex justify-center">
            <div class="increment-div d-flex justify-center">
              <v-icon
                color="white"
                class="common-icon minus-icon"
                @click="actionButton(false)"
              >
                mdi-minus
              </v-icon>
              <p class="incr-p">{{ count }}</p>
              <v-icon
                color="white"
                class="common-icon plus-icon"
                @click="actionButton(true)"
              >
                mdi-plus
              </v-icon>
            </div>
          </div>
        </v-card-text> -->

        <v-card-actions class="pb-6">
          <v-btn
            color="#1FE2C4"
            block
            @click="add_variant_item"
            :disabled="selectedVariants.length !== parentItem.attributes.length"
          >
            <span class="btn-title">Add To Bag</span>
            <!-- <span class="total-price">Rs.{{ totalPrice }}</span> -->
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from "../../bus";
export default {
  data: () => ({
    varaintsDialog: false,
    parentItem: null,
    items: null,
    filters: {},
    filterdItems: [],

    //
    panel: [],
    addOnpanel: [],
    variantRadio: {},
    selectedValues: [],
    payload_string: "",
    variantMatch: "",
    payloadArray: [],
    variantCheckbox: {}, // Initialize variantCheckbox to keep track of selections

    menuArray: [
      {
        title: "Choose Your Combination",
        required: true,
        valueSelect: false,
      },
      {
        title: "Choose Your Flavor",
        required: true,
        valueSelect: false,
      },
      {
        title: "Add a Drink",
        valueSelect: false,
      },
      {
        title: "Add Extra",
        valueSelect: false,
      },
      {
        title: "Add Apeteasers",
        valueSelect: false,
      },
    ],

    radioOptions: [
      {
        label: "On its own",
        value: "On its own",
        price: 100,
      },
      {
        label: "With 2 Reg Slides",
        value: "With 2 Reg Slides",
        price: 200,
      },
      // { label: "Radio 3", value: "radio3", price: 300 },
      // { label: "Radio 4", value: "radio4", price: 400 },
    ],
  
    selectedRadio: null,
    selectedVariants: [],
    selectedAddOn: [],
    selectedSpecificItems:[],

    count: 1,
    totalAmount: 0,
  }),

  methods: {
    close_dialog() {
      this.varaintsDialog = false;
      this.panel = [];
      this.addOnpanel = [];
      this.selectedValues = [];
      this.selectedAddOn = [];
      this.selectedVariants = [];
      this.variantRadio = {};
      this.variantCheckbox = {};
    },
    formtCurrency(value) {
      value = parseFloat(value);
      return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,");
    },
    updateFiltredItems() {
      this.$nextTick(function () {
        const values = [];
        Object.entries(this.filters).forEach(([key, value]) => {
          if (value) {
            values.push(value);
          }
        });

        if (!values.length) {
          this.filterdItems = this.variantsItems;
        } else {
          const itemsList = [];
          this.filterdItems = [];
          this.variantsItems.forEach((item) => {
            let apply = true;
            item.item_attributes.forEach((attr) => {
              if (
                this.filters[attr.attribute] &&
                this.filters[attr.attribute] != attr.attribute_value
              ) {
                apply = false;
              }
            });
            if (apply && !itemsList.includes(item.item_code)) {
              this.filterdItems.push(item);
              itemsList.push(item.item_code);
            }
          });
        }
      });
    },
    add_item(item) {
      evntBus.$emit("add_item", item);
      this.close_dialog();
    },
    actionButton(key) {
      if (key) {
        this.count += 1;
      } else {
        if (this.count > 1) {
          this.count -= 1;
        }
      }
    },

    calculateTotalForSelected(selectedArray, optionsArray) {
      return selectedArray.reduce((total, selectedValue) => {
        const option = optionsArray.find(
          (option) => option.value === selectedValue
        );
        return option ? total + option.price : total;
      }, 0);
    },
    add_variant_item() {
      const vm = this;
      const merageArray = [...this.payloadArray, ...this.selectedAddOn];
      const filteredArray = merageArray.filter((item) => item != null);
      const obj = {
        items: filteredArray,
        item_specifics:vm.selectedSpecificItems
      };
      frappe.call({
        method: "neighborhood_pos.neighborhood_pos.api.posapp.create_bundle_from_item",
        args: {
          json_data: {items:[obj]}
        },
        callback: function (r) {
          if (r.message) {
            console.log("r.mess",r.message[0][0])
            vm.panel = [];
            vm.selectedValues = [];
            r.message[0][0].item_name = r.message[0][0].item_code;
            evntBus.$emit("add_item", r.message[0][0]);
            vm.varaintsDialog = false;
            vm.selectedVariants = [];
            vm.selectedAddOn = [];
            vm.variantRadio = {};
            vm.selectedAddOn = [];
            vm.panel = [];
            vm.addOnpanel = [];
            vm.payloadArray = [];
            vm.variantMatch = "";
          }
        },
      });
    },
    onRadioChange(index, selectedValue) {
      console.log(`Index: ${index}, Selected Value:`, selectedValue);
      this.parentItem.attributes[index].valueSelect = true;
      this.selectedVariants[index] = selectedValue;
      const selectedNamesString = this.selectedVariants
        .map((variant) => variant.abbr)
        .join("-");

      this.payload_string = `${this.parentItem.item_name}-${selectedNamesString}`;
      console.log(" this.payload_string", this.payload_string);
      this.variantMatch = this.parentItem.variants.filter((item) => {
        return this.payload_string === item.item_code;
      })[0];
      console.log("variantMatch", this.variantMatch);
      if (this.variantMatch) {
        if (this.selectedVariants.length == this.parentItem.attributes.length) {
          const obj = {
            item_code: `${this.variantMatch.item_code}`,
            item_group: this.variantMatch.item_group,
            qty: 1,
            rate: this.variantMatch.rate,
          };
          this.payloadArray.push(obj);
          console.log("  this.payloadArray", this.payloadArray);
        }
        this.parentItem?.add_ons.forEach((item) => {
          console.log("add-item", item);
          if (item?.dependent_item == this.payload_string) {
            item.hide = false;
          }
        });
      }
      // if (
      //   this.selectedVariants.length == this.parentItem.attributes.length &&
      //   !this.variantMatch
      // ) {
      //   const obj = {
      //     color: "red",
      //     text: "Item not Found",
      //   };
      //   evntBus.$emit("show_mesage", obj);
      // }
    },
    addOnChange(index, selectedValue) {
      console.log(`Index: ${index}, Selected Value-add-on:`, selectedValue);
      const obj = {
        item_code: selectedValue.item_name,
        item_group: selectedValue.item_group,
        qty: 1,
        rate: selectedValue.rate,
      };
      this.selectedAddOn[index] = obj;
    },
  },
  computed: {
    variantsItems() {
      if (!this.parentItem) {
        return [];
      } else {
        return this.items.filter(
          (item) => item.variant_of == this.parentItem.item_code
        );
      }
    },
    totalPrice() {
      let total = 0;

      // if(this.payloadArray.length>0){
      //   console.log("enter in computed......")
      //  for (let index = 0; index < this.payloadArray.length; index++) {
      //   total = total + this.payloadArray[index].rate;
      //   }
      // }
      // if(this.selectedAddOn.length>0){
      //   for (let index = 0; index < this.selectedAddOn.length; index++) {
      //   total = total + this.selectedAddOn[index].rate;
      //   }
      // }

      return total;
    },
  },
  watch: {
    selectedValues: {
      handler(newVal, oldVal) {
        if (Array.isArray(newVal)) {
          let flattenedArray = newVal?.flat();
          this.selectedAddOn = [];
          this.selectedSpecificItems=[]
          flattenedArray.forEach((item) => {
            console.log("watcher...",item)
            if(item.parentfield=="item_add_ons"){
            const obj = {
              item_code: item.item_name,
              item_group: item.item_group,
              qty: 1,
              rate: item.rate,
            };
            this.selectedAddOn.push(obj);
          }
          if(item.parentfield=="item_specifics"){
            const obj = {
              name:item.display_name
            };
            this.selectedSpecificItems.push(obj);
          }

          });
        }
      },
      deep: true,
    },
  },

  created: function () {
    evntBus.$on("open_variants_model", (item, items, variants) => {
      console.log("ava-variants",variants)
      variants[0].add_ons.forEach((item)=>{
        if(item.item_type=="Item Specifics"){
          item.item_specifics.forEach((i)=>{
            i.display_name=i.item_specifics_name
          })
          item.item_add_ons=item.item_specifics



        }
      })
      this.varaintsDialog = true;
      this.parentItem = item || null;
      this.parentItem.add_ons = variants[0].add_ons;
      this.parentItem.variants = variants[0].variants;
      // this.parentItem?.add_ons.forEach((item) => {
      //   if (item?.is_dependent) {
      //     item.hide = true;
      //   }
      // });

      this.items = items;
      this.filters = {};
      this.$nextTick(function () {
        this.filterdItems = this.variantsItems;
      });
      this.parentItem?.attributes.forEach((item) => {
        item.required = true;
        item.valueSelect = false;
      });
    });
  },
};
</script>
<style scoped>
.v-expansion-panel:not(:first-child):after {
  border-top: none !important;
}
.title-p {
  font-size: 30px;
  font-weight: 500;
}
.parent-p {
  font-size: 20px;
  font-weight: 500;
}
.dialog-main {
  overflow-x: hidden !important;
}
.panel-item {
  padding-top: 0px !important;
  padding-bottom: 0px !important;
}
.panel-item:hover {
  background: #edf2f6;
}
.total-price {
  position: absolute;
  left: 443px;
  width: 140px;
  margin-right: 24px;
  text-transform: capitalize;
}
.btn-title {
}
.increment-div {
  /* border: 1px solid black; */
  width: 121px;
  border-radius: 24px;
  background: #edf2f6;
  height: 35px;
}
.common-icon {
  border: 1px solid black;
  border-radius: 30px;
  width: 35px;
  margin-top: 2px;
  margin-bottom: 2px;
  background: black;
}
.minus-icon {
  right: 15px;
}
.plus-icon {
  left: 15px;
}
.add-on-div {
  position: relative;
  bottom: 14px;
}
.incr-p {
  font-size: 20px;
  top: 8px;
  position: relative;
}
.header-font {
  font-size: 15px;
  font-weight: 500;
  min-height: 48px !important;
}
.context-bg {
  background: #edf2f6;
}
.radio-div {
  height: 40px;
}
.required-p {
  position: relative;
  top: 8px;
  right: 8px;
  color: red;
  font-size: 12px;
  text-transform: uppercase;
}
.added-p {
  position: relative;
  top: 8px;
  right: 8px;
  color: white;
  font-size: 14px;
  background: #8bc24a;
  width: 57px;
  padding-left: 8px;
  height: 23px;
  padding-top: 6px;
  border-radius: 4px;
  font-weight: 500;
}
.add-on-title {
  color: black;
  font-size: 18px;
}
.add-on-content {
  position: relative;
  bottom: 28px;
}

::v-deep(.radio-button .v-label) {
  font-size: 14px !important;
  top: 4px !important;
  position: relative !important;
}
::v-deep(.radio-button .v-icon.v-icon) {
  font-size: 22px !important;
  bottom: 4px !important;
  position: relative !important;
}
</style>
