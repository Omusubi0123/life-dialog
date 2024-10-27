export default function createDatePickerOption() {
    const option = {
        "root": {
          "base": "relative",
          "input": {
            "base": "bg-red-500 w-full text-sm font-semibold text-gray-900 bg-white rounded-lg dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:ring-2 focus:ring-cyan-300",
            "addon": "",
            "field": {
              "base": "relative",
              "icon": {
                "base": "absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none",
                "svg": "w-4 h-4 text-gray-500 dark:text-gray-400"
              },
              "rightIcon": {
                "base": "",
                "svg": ""
              },
              "input": {
                "base": "ps-10 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg block w-full dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white  datepicker-input in-edit",
                "sizes": {
                  "sm": "text-sm",
                  "md": "text-sm",
                  "lg": "text-base"
                },
                "colors": {
                  "gray": "text-gray-900 bg-white dark:bg-gray-700 dark:text-white dark:border-gray-600 focus:ring-2 focus:ring-cyan-300",
                  "info": "text-blue-900 bg-blue-100 dark:bg-blue-700 dark:text-white dark:border-blue-600 focus:ring-2 focus:ring-blue-300",
                  "failure": "text-red-900 bg-red-100 dark:bg-red-700 dark:text-white dark:border-red-600 focus:ring-2 focus:ring-red-300",
                  "warning": "text-yellow-900 bg-yellow-100 dark:bg-yellow-700 dark:text-white dark:border-yellow-600 focus:ring-2 focus:ring-yellow-300",
                  "success": "text-green-900 bg-green-100 dark:bg-green-700 dark:text-white dark:border-green-600 focus:ring-2 focus:ring-green-300"
                },
                "withIcon": {
                  "off": "",
                  "on": ""
                },
                "withRightIcon": {
                  "off": "",
                  "on": ""
                },
                "withAddon": {
                  "off": "",
                  "on": ""
                },
                "withShadow": {
                  "off": "",
                  "on": ""
                }
              }
            }
          }
        },
        "popup": {
          "root": {
            "base": "absolute top-10 z-50 block pt-2",
            "inline": "relative top-0 z-auto",
            "inner": "inline-block rounded-lg bg-white p-4 shadow-lg dark:bg-gray-700"
          },
          "header": {
            "base": "",
            "title": "px-2 py-3 text-center font-semibold text-gray-900 dark:text-white",
            "selectors": {
              "base": "mb-2 flex justify-between",
              "button": {
                "base": "rounded-lg bg-white px-5 py-2.5 text-sm font-semibold text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600",
                "prev": "",
                "next": "",
                "view": ""
              }
            }
          },
          "view": {
            "base": "p-1"
          },
          "footer": {
            "base": "mt-2 flex space-x-2",
            "button": {
              "base": "w-full rounded-lg px-5 py-2 text-center text-sm font-medium focus:ring-4 focus:ring-cyan-300",
              "today": "bg-cyan-700 text-white hover:bg-cyan-800 dark:bg-cyan-600 dark:hover:bg-cyan-700",
              "clear": "border border-gray-300 bg-white text-gray-900 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:hover:bg-gray-600"
            }
          }
        },
        "views": {
          "days": {
            "header": {
              "base": "mb-1 grid grid-cols-7 bg-white",
              "title": "h-6 text-center text-sm font-medium leading-6 text-gray-500 dark:text-gray-400"
            },
            "items": {
              "base": "grid w-64 grid-cols-7 bg-white text-center",
              "item": {
                "base": "bg-white flex-1 p-0 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600",
                "selected": "text-center bg-cyan-700 text-white hover:bg-cyan-600",
                "disabled": "text-gray-500"
              }
            }
          },
          "months": {
            "items": {
              "base": "grid w-64 grid-cols-4 bg-white",
              "item": {
                "base": "bg-white block flex-1 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600",
                "selected": "bg-cyan-700 text-white hover:bg-cyan-600",
                "disabled": "text-gray-500"
              }
            }
          },
          "years": {
            "items": {
              "base": "grid w-64 grid-cols-4 bg-white",
              "item": {
                "base": "bg-white block flex-1 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600",
                "selected": "bg-cyan-700 text-white hover:bg-cyan-600",
                "disabled": "text-gray-500"
              }
            }
          },
          "decades": {
            "items": {
              "base": "grid w-64 grid-cols-4 bg-white",
              "item": {
                "base": "bg-white block flex-1 cursor-pointer rounded-lg border-0 text-center text-sm font-semibold leading-9 text-gray-900 hover:bg-gray-100 dark:text-white dark:hover:bg-gray-600",
                "selected": "bg-cyan-700 text-white hover:bg-cyan-600",
                "disabled": "text-gray-500"
              }
            }
          }
        }
      };
    return option;
}