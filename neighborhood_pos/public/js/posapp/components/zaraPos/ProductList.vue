<template>
  <v-card elevation="2" class="border-16 product-main-card">
    <!-- Categories Section -->
    <v-row>
      <v-col cols="12">
        <p class="pt-6 pl-6 title-h">Categories</p>
        <v-row
          class="px-4 ml-1 category-row"
          style="
            overflow-x: auto;
            white-space: nowrap;
            scrollbar-width: thin;
            -webkit-overflow-scrolling: touch;
          "
        >
          <v-col
            v-for="category in categories"
            :key="category"
            cols="auto"
            class="px-0 py-1"
            style="display: inline-block"
          >
            <v-btn
              variant="outlined"
              size="large"
              class="ma-2 text-capitalize"
              :class="{
                'active-catgory': selectedCategory === category,
                'unactive-catgory': selectedCategory !== category,
              }"
              :color="selectedCategory === category ? '#21a0a0' : '#D3ECEC'"
              @click="changeCategory(category)"
              style="white-space: normal"
            >
              <p class="black--text mt-2 category-p">
                {{ category.item_group }}
              </p>
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row class="px-2">
      <v-col cols="12">
        <p class="pt-6 pl-5 title-h">Products</p>
      </v-col>
    </v-row>
    <v-row class="px-10 pb-0" v-show="filteredProducts.length > 0">
      <!-- Product Cards -->
      <v-col
        v-for="product in filteredProducts"
        :key="product.item_code"
        cols="12"
        sm="6"
        md="4"
        lg="3"
        xl="3"
        class="mb-4 pt-0"
      >
        <v-card class="hover-card" elevation="0" @click="openDialog(product)">
          <img
            :src="product.image ? product.image : defaultImg"
            class="white--text align-end item-img"
          />

          <div style="display: flex; justify-content: space-between">
            <div style="width: 140px">
              <v-card-title class="item-name py-0 mt-3">{{
                product.item_name
              }}</v-card-title>
              <v-tooltip activator="parent" location="top">{{
                product.item_name
              }}</v-tooltip>

              <v-card-subtitle class="item-price mb-2"
                >Rs.{{ formatNumber(product.rate) }}</v-card-subtitle
              >
            </div>
            <div>
              <div class="stock-div">
                <p
                  class="stock-count"
                  :class="{ 'negative-stock': product.actual_qty < 0 }"
                >
                  {{ product.actual_qty }}
                </p>
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-show="filteredProducts.length == 0 && !itemloading">
      <v-col cols="12" style="display: flex; justify-content: center">
        <img
          src="/assets/neighborhood_pos/js/posapp/components/pos/noData.png"
          alt=""
          class="ml-5"
        />
      </v-col>
    </v-row>
    <v-row v-show="itemloading">
      <v-col cols="12" style="display: flex; justify-content: center">
        <v-progress-circular
          :size="100"
          :width="7"
          color="#21a0a0"
          indeterminate
        ></v-progress-circular>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from "vue";

import eventBus from "../../bus";
import indexedDBService from "../../indexedDB";

// Reactive data
const categories = ref([]);
const pos_profile = ref("");
const selectedCategory = ref("");
const searchValue = ref("");
const defaultImg = ''
const orderType = ref("");

const isOnline = ref(navigator.onLine);
const pollingInterval = 4000; // Set the desired interval (e.g., 5000 ms for 5 seconds)
let intervalId = ref(null);

let checkConnectionInterval = null;
const requestComplete = ref(false);
const itemloading = ref(false);
const getAllItems = ref(false);
const offlineMode = ref(false);
const unsyncInvoice = ref(0);

const products = ref([
  // {
  //   name: "GUL-BAHAAR2",
  //   price: "Rs.270,000",
  //   image:
  //     "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNpb2VT-9JGAOD7MWVQHlKtq5czfD1yHaLlg&s",
  // },
]);
const filteredProducts = computed(() => {
  // If the search value is empty, return all products
  if (!searchValue.value) {
    return products.value;
  }
  // Otherwise, filter products that match the search value (case insensitive)
  return products.value.filter((product) =>
    product.item_code.toLowerCase().includes(searchValue.value.toLowerCase())
  );
});
const formatNumber = (num) => {
  return new Intl.NumberFormat("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num);
};
const handleOffline = () => {
  isOnline.value = false;
  console.log("Internet connection lost.");
  clearInterval(intervalId.value);
  intervalId.value = null;
  // products.value = [];
  // products.value = JSON.parse(localStorage.getItem("items_storage"));
  eventBus.emit("set_all_items", products.value);
  // triggerOfflineFunction();  // Call your function to handle offline actions
  indexedDBService
    .openDatabase()
    .then(() => {
      return indexedDBService.getGroupItems();
    })
    .then((data) => {
      categories.value = [];
      categories.value = data;
      selectedCategory.value = categories.value[0];
      const allItems =
        JSON.parse(localStorage.getItem("All-items_storage")) || [];

      // Filter items based on the selected category
      const filteredItems = allItems.filter(
        (item) =>
          item.item_group === selectedCategory.value.item_group &&
          item.order_type == orderType.value
      );
      products.value = [];
      // Store the filtered items in products
      products.value = filteredItems;
    })
    .then(() => {
      console.log("Customer Info Data extracted successfully");
    })
    .catch((error) => {
      console.error("Error with IndexedDB operation:", error);
    });
};
const handleOnline = () => {
  isOnline.value = true;

  if (isOnline.value && !intervalId.value) {
    // syncSalesInvoicesFromIndexedDB();
    intervalId.value = setInterval(
      syncSalesInvoicesFromIndexedDB,
      pollingInterval
    );
  } else {
    // console.log("else clear interval")
    // clearInterval(intervalId.value);
    // intervalId.value = null;
  }
};
// const syncData = () => {
//   console.log("Syncing data with the server...");
//   // Add your data-syncing code here
// };
const syncSalesInvoicesFromIndexedDB = async () => {
  /**
   * This method executes the flow of synchronization of sales_invoice saved in indexedDB.
   *
   * @param {None} -
   * @returns {None} - Gives a console log mentioning if the record synchronization is true.
   */
  try {
    // Await the promise returned by openDatabase
    const db = await indexedDBService.openDatabase();
    //console.log("Database opened successfully.");

    // Fetch unsynced records
    const allRecords = await fetchUnsyncedSalesInvoiceRecords(db);
    console.log("Fetched unsynced records:", allRecords);
    console.log("Fetched unsynced records length:", allRecords.length);
    unsyncInvoice.value = allRecords.length;
    eventBus.emit("Unsync-record", unsyncInvoice.value);

    if (allRecords.length == 0) {
      console.log("no data availabe for syning");
      // indexedDBService
      //   .openDatabase()
      //   .then(() => {
      //     return indexedDBService.clearCreateInvoice();
      //   })
      //   .then(() => {
      //     console.log("get response create_invoice table cleared successfully");
      //   })
      //   .catch((error) => {
      //     console.error("Error get offers:", error);
      //   });
      clearInterval(intervalId.value);
      intervalId.value = null;
      return;
    }

    // checkConnection();

    // Sync each record
    if (!requestComplete.value) {
      for (const record of allRecords) {
        //console.log("Syncing record:", record);
        // if (record.invoice.name) {
        //   console.log("Invoice name", record.invoice.name);
        //   // checkConnection();
        //   await syncSalesInvoiceRecord(db, record); // Await each sync operation
        // }
        //  else {
        //   // checkConnection();
        //   record.invoice = await updateInvoice(record);

        //   // try {
        //   //   const db = await indexedDBService.openDatabase();
        //   //   // Update the invoice with the provided invoice data (record.invoice)
        //   //   record.invoice = await indexedDBService.updateSalesInvoice(
        //   //     record.id,
        //   //     record
        //   //   );
        //   //   console.log("Record ID after calling the update invoice:", record.id);
        //   // } catch (error) {
        //   //   console.error("Error updating or syncing invoice:", error);
        //   // }

        //   // checkConnection();
        //   await syncSalesInvoiceRecord(db, record); // Await each sync operation
        //   console.log("Sync Invoice Record ID:", record.id);
        // }
        await syncSalesInvoiceRecord(db, record); // Await each sync operation
        console.log("Sync Invoice Record ID:", record.id);
      }
    }
  } catch (error) {
    console.error("Error during synchronization:", error);
  }
};

const fetchUnsyncedSalesInvoiceRecords = async (db) => {
  /**
   * Fetches unsynced sales invoice records from IndexedDB.
   *
   * @param {Object} db - The database instance.
   * @returns {Promise<Array>} - A promise that resolves to an array of unsynced records.
   */
  try {
    const transaction = db.transaction(["create_invoice"], "readonly");
    const objectStore = transaction.objectStore("create_invoice");
    const unsyncedRecords = [];

    // Open a cursor to iterate over all records
    return await new Promise((resolve, reject) => {
      const request = objectStore.openCursor();

      request.onsuccess = (event) => {
        const cursor = event.target.result;
        if (cursor) {
          const record = cursor.value;

          // Check if the record is unsynced
          if (record.synced === false) {
            unsyncedRecords.push(record);
          }

          // Move to the next record
          cursor.continue();
        } else {
          // No more records, resolve with the filtered array
          resolve(unsyncedRecords);
        }
      };

      request.onerror = (event) => {
        reject(event.target.error);
      };
    });
  } catch (error) {
    console.error("Error fetching unsynced records:", error);
    throw error;
  }
};

const syncSalesInvoiceRecord = async (db, record) => {
  let load = JSON.parse(JSON.stringify(record));
  // console.log("load offline invoice", load);

  // Fetch the offline invoice log before submitting
  // await getInvoiceLog();

  // load.invoice.payments.forEach((payment) => {
  //   if (payment.mode_of_payment === load.mode_of_payment) {
  //     payment.amount = load.invoice.rounded_total;
  //   }
  //   // if (offlineModeOfPayment.value === "") {
  //   //   load.invoice.payments[0].amount = load.invoice.rounded_total;
  //   // }
  // });

  try {
    console.log("Making submit API call with payload:", load);
    requestComplete.value = true;
    const response = await new Promise((resolve, reject) => {
      // console.log("inPromises", load);
      // checkConnection();
      frappe.call({
        method: "neighborhood_pos.neighborhood_pos.api.posapp.sales_invoice",
        args: {
          data: load.data,
          invoice: load.invoice,
          taxvalue: load.taxvalue || "",
        },
        callback: (response) => {
          // console.log("API call response:", response);
          requestComplete.value = false;

          if (!response.exc && response.message && response.message.name) {
            console.log(
              "API call was successful. Invoice synced:",
              response.message.name
            );
            resolve(response);
          } else {
            console.error(
              "API call failed. Response:",
              response.exc || response
            );
            reject(
              response.exc || new Error("Failed to sync sales invoice record")
            );
          }
        },
      });
    });

    // console.log("Marking record as synced with ID:", load.id);
    await markRecordAsSynced(db, load);
    console.log("Record marked as synced successfully.");

    return response;
  } catch (error) {
    console.error("An error occurred during the sync process:", error);
    return Promise.reject(error);
  }
};

const updateInvoice = async (doc) => {
  requestComplete.value = true;
  let load = JSON.parse(JSON.stringify(doc));
  //console.log("in Update invoice...", load);
  // load.invoice.payments.forEach((payment) => {
  //   if (payment.mode_of_payment === load.mode_of_payment) {
  //     payment.amount = load.invoice.rounded_total;
  //   }
  // });

  try {
    const result = await new Promise((resolve, reject) => {
      // Initiate the API call using frappe.call
      frappe.call({
        method: "neighborhood_pos.neighborhood_pos.api.posapp.update_invoice",
        args: {
          data: load.invoice,
        },
        async: true,
        callback: (r) => {
          if (r && r.message) {
            // r.message.grand_total=
            resolve(r.message);
          } else {
            reject("Error: No message returned from API");
          }
        },
        error: (error) => {
          reject(error);
        },
      });
    });

    // console.log("API call result:", result);
    return result;
  } catch (error) {
    console.error("Error during API call:", error);
    throw error;
  }
};

const getInvoiceLog = async () => {
  try {
    await indexedDBService.openDatabase(); // Open the database

    const data = await indexedDBService.getUpdateInvoice("Sales Invoice");
    console.log("get-indexed-db-invoice", data);

    // offlineInvoiceData.value = JSON.parse(JSON.stringify(data)); // Deep copy the data
    // console.log("Invoice saved successfully");

    // offlineTotalAmount.value = await offlineTotalPayment(); // Set offline total amount
  } catch (error) {
    console.error("Error with IndexedDB operation:", error);
    throw error; // Propagate the error
  }
};

async function markRecordAsSynced(db, record) {
  try {
    // Assuming the record ID is stored as id, replace with actual key property if necessary
    const recordId = record.id || record.key || record.recordId;

    if (!recordId) {
      throw new Error("Record does not have a valid key or id");
    }

    const transaction = db.transaction(["create_invoice"], "readwrite");
    const objectStore = transaction.objectStore("create_invoice");

    const request = objectStore.get(recordId);

    request.onsuccess = () => {
      const existingRecord = request.result;
      if (existingRecord) {
        existingRecord.synced = true; // Mark as synced

        const updateRequest = objectStore.put(existingRecord);

        updateRequest.onsuccess = () => {
          console.log(`Record with ID ${recordId} marked as synced.`);
        };

        updateRequest.onerror = (event) => {
          console.error("Error updating the record:", event.target.errorCode);
        };
      } else {
        console.error(`Record with ID ${recordId} not found.`);
      }
    };

    request.onerror = (event) => {
      console.error(
        "Error retrieving record for syncing:",
        event.target.errorCode
      );
    };
  } catch (error) {
    console.error("Error in markRecordAsSynced:", error);
  }
}

// offline syncing end

// Event handling
const openDialog = (product, flag = false) => {
  // console.log("Product clicked:", product);
  product.qty = 1;
  const obj = {
    product,
    flag,
  };
  eventBus.emit("open-product-dialog", obj);
};
const changeCategory = (category) => {
  selectedCategory.value = category;
  // console.log("selectedCategory", selectedCategory.value);
  getAllItems.value =
    JSON.parse(localStorage.getItem("get-all-item-status")) || false;
  console.log("getAllItems.value", getAllItems.value);

  if (getAllItems.value) {
    const allItems =
      JSON.parse(localStorage.getItem("All-items_storage")) || [];

    // Filter items based on the selected category
    const filteredItems = allItems.filter(
      (item) =>
        item.item_group === selectedCategory.value.item_group &&
        item.order_type == orderType.value
    );
    products.value = [];
    // Store the filtered items in products
    products.value = filteredItems;

    console.log("Filtered Products:", products.value);
  } else {
    get_items(pos_profile.value, selectedCategory.value);
  }
};
const scanItem = (category) => {
  const allItems = JSON.parse(localStorage.getItem("All-items_storage")) || [];

  // Check for an exact match with item_code
  const exactMatchItem = allItems.find(
    (item) => item.item_code.toLowerCase() == searchValue.value.toLowerCase()
  );
  if (searchValue.value) {
    if (exactMatchItem) {
      // Emit an event for the exact match
      console.log("Exact match found:", exactMatchItem);
      exactMatchItem.qty = 1;
      eventBus.emit("add-to-cart", exactMatchItem);
    } else {
      eventBus.emit("show_mesage", {
        text: "No item found",
        color: "error",
      });
    }
  }
  eventBus.emit("clear-search");
};
const get_items = async (pos_profile, groupItem) => {
  // console.log("groupItem", selectedCategory.value);

  if (navigator.onLine) {
    try {
      const response = await frappe.call({
        method: "neighborhood_pos.neighborhood_pos.api.posapp.get_items",
        args: {
          pos_profile: pos_profile,
          price_list: "",
          item_group: groupItem.item_group,
          search_value: "",
          customer: "Walk in",
          order_type: orderType.value,
        },
      });

      if (response.message) {
        // console.log("get-items1", response.message, response.message.length);
        products.value = [];
        products.value = response.message;
        itemloading.value = false;
        // Store in localStorage
        localStorage.setItem("items_storage", JSON.stringify(response.message));

        // Save items in IndexedDB
        indexedDBService
          .openDatabase()
          .then((db) => {
            // Save POS Profile and POS Opening Shift in IndexedDB
            return Promise.all([
              indexedDBService.saveItems(JSON.stringify(products.value)),
            ]);
          })
          .then(() => {
            console.log("Product item saved successfully in Db");
          })
          .catch((error) => {
            console.error("Error saving to IndexedDB:", error);
          });
        // await indexedDBService.openDatabase();
        // await indexedDBService.saveItems(products.value);

        console.log("Items saved successfully!");
      }
    } catch (error) {
      console.error("Error saving Items:", error);
    }
  } else {
    handleOffline();
  }
};
// const loadAllItems = async (pos_profile, groupItem) => {
//   if (navigator.onLine) {
//     try {
//       const response = await frappe.call({
//         method: "neighborhood_pos.neighborhood_pos.api.posapp.get_items",
//         args: {
//           pos_profile: pos_profile,
//           price_list: "",
//           item_group: "",
//           search_value: "",
//           customer: "Walk in",
//           order_type: orderType.value,
//         },
//       });

//       if (response.message) {
//         getAllItems.value = true;
//         // Store in localStorage
//         localStorage.setItem(
//           "All-items_storage",
//           JSON.stringify(response.message)
//         );
//         console.log("Load All Items", response.message);
//       }
//     } catch (error) {
//       console.error("Error saving Items:", error);
//     }
//   } else {
//     // handleOffline();
//   }
// };
const loadAllItems = async (pos_profile) => {
  if (navigator.onLine) {
    try {
      const allItems = []; // To store combined results for all order types

      // Loop through each order type in pos_profile.against_applicable_for_order_type
      for (const order of pos_profile.applicable_for_order_type) {
        const orderType = order.order_type; // Get the order type

        const response = await frappe.call({
          method: "neighborhood_pos.neighborhood_pos.api.posapp.get_items",
          args: {
            pos_profile: pos_profile,
            price_list: "",
            item_group: "",
            search_value: "",
            customer: "Walk in",
            order_type: orderType,
          },
        });

        if (response.message) {
          // Add order type to each item in the response
          const itemsWithOrderType = response.message.map((item) => ({
            ...item,
            order_type: orderType,
          }));

          // Add to the allItems array
          allItems.push(...itemsWithOrderType);
        }
      }

      // Store combined results in localStorage
      localStorage.setItem("All-items_storage", JSON.stringify(allItems));
      console.log("All items loaded and stored:", allItems);

      // Update status after all API calls are completed
      getAllItems.value = true;
      localStorage.setItem(
        "get-all-item-status",
        JSON.stringify(getAllItems.value)
      );
    } catch (error) {
      console.error("Error loading items:", error);
    }
  } else {
    //     // handleOffline();
  }
};
const offlineProfileData = async () => {
  try {
    // Wait for the IndexedDBService to open the database and get the pos_profile
    const data = await indexedDBService
      .openDatabase()
      .then(() => indexedDBService.getPosProfile());

    // console.log("offline pos profile from order summary", data);

    if (data && data.length > 0) {
      pos_profile.value = data[0];
    } else {
      console.error("No profile data found in IndexedDB.");
    }
  } catch (error) {
    console.error("Error with IndexedDB operation getting profile:", error);
  }
};

const checkInternetConnection = async () => {
  try {
    console.log("internetConnection", navigator.onLine);
    // const response = await fetch("https://www.google.com", { mode: "no-cors" });
    // if (response) {
    //   isOnline.value = true;
    // }
  } catch (error) {
    isOnline.value = false;
    // triggerOfflineFunction();
  }
};
watch(offlineMode, (newStatus) => {
  if (newStatus) {
    handleOffline();
    offlineProfileData();
  } else {
    handleOnline();
  }
});
onMounted(() => {
  localStorage.setItem("get-all-item-status", false);
  window.addEventListener("offline", () => {
    console.log("You are offline");
    handleOffline();
  });

  window.addEventListener("online", () => {
    console.log("You are online");
    handleOnline();
  });
  handleOnline();
  // checkConnectionInterval = setInterval(checkInternetConnection, 5000);  // Every 5 seconds
  eventBus.on("sync-offline-invoice", () => {
    if (navigator.onLine) {
      syncSalesInvoicesFromIndexedDB();
    }
  });

  eventBus.on("search-item", (value) => {
    // console.log("receive-search", value);
    searchValue.value = value;
    scanItem();
  });
  eventBus.on("send_order_type", (data) => {
    orderType.value = data;
  });
  eventBus.on("send_pos_profile", async (profile) => {
    console.log("pos-profile", profile);
    pos_profile.value = profile;
    categories.value = profile.item_groups;
    selectedCategory.value = categories.value[0];

    const getItemsStatus =
      JSON.parse(localStorage.getItem("get-all-item-status")) || false;

    if (!getItemsStatus) {
      loadAllItems(pos_profile.value);
    }
    if (profile) {
      await indexedDBService
        .openDatabase()
        .then((db) => {
          // Save POS Profile and POS Opening Shift in IndexedDB
          return Promise.all([
            indexedDBService.saveItemGroups(
              JSON.stringify(profile.item_groups)
            ),
          ]);
        })
        .then(() => {
          console.log("In component Items Groups data saved to IndexedDB");
        })
        .catch((error) => {
          console.error("Error saving to IndexedDB:", error);
        });
    }
    // get_items(profile, selectedCategory.value);
  });

  eventBus.on("update_get_item", (data) => {
    // console.log("received-order", data);
    orderType.value = data;
    const getItemsStatus =
      JSON.parse(localStorage.getItem("get-all-item-status")) || false;
    // console.log("getItemsStatus", getItemsStatus);
    if (!getItemsStatus) {
      get_items(pos_profile.value, selectedCategory.value, data);
    } else {
      changeCategory(selectedCategory.value);
    }
    // loadAllItems(pos_profile.value, selectedCategory.value);
  });
  eventBus.on("open-product-menu", () => {
    if (navigator.onLine) {
      get_items(pos_profile.value, selectedCategory.value);
      loadAllItems(pos_profile.value, selectedCategory.value);
    }
  });
  eventBus.on("app-internet-status", (newStatus) => {
    offlineMode.value = !newStatus;
  });
  // eventBus.on('sync-offline-invoice',()=>{

  // })
});
onUnmounted(() => {
  window.removeEventListener("offline", handleOffline);
  window.removeEventListener("online", handleOnline);
});
</script>

<style scoped>
.category-row {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  -ms-overflow-style: none; /* Internet Explorer 10+ */
  scrollbar-width: none; /* Firefox */
}
.product-main-card {
  max-height: 80vh;
  height: 80vh;
  overflow-y: scroll;
  overflow-x: hidden;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2) !important;
}
.hover-card {
  border-radius: 16px;
}
.hover-card:hover {
  transform: translateY(-5px);
  transition: transform 0.3s;
}
.stock-div {
  border: 1px solid #fcdfd3;
  width: 26px;
  border-radius: 4px;
  height: 25px;
  margin-top: 20px;
  /* margin-right: 14px; */
  padding-left: 8px;
  padding-top: 1px;
  background: #fcdfd3;
  position: relative;
  right: 7px;
}
.stock-count {
  color: black;
  font-size: 12px;
  width: 80px !important;
  position: relative;
  right: 0px;
}
.item-img {
  border-top-left-radius: 13px !important;
  border-top-right-radius: 13px !important;
  width: 350px;
  height: 140px;
}
.item-name {
  font-size: 14px;
  font-weight: 400;
  font-family: Noto Sans;
}
.item-price {
  font-size: 14px;
  font-weight: 700;
  color: #f05d23 !important;
  font-family: Noto Sans;
}
.title-h {
  font-size: 16px;
  font-weight: 600;
  font-family: Noto Sans;
}
.category-p {
  color: black !important;
}
.unactive-catgory {
  background-color: #d3ecec !important;
  border-radius: 8px !important;
  border: 1px solid #21a0a0 !important;
}
.active-catgory {
  background-color: #fcdfd3 !important;
  border-radius: 8px !important;
  border: 1px solid #f05d23 !important;
}
.negative-stock {
  width: 60px;
  position: relative;
  right: 4px;
}
</style>
