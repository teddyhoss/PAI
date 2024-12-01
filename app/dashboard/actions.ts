"use server";

export async function getTotalReports() {
  try {
    return "23";
  } catch (error) {
    console.error(error);
    throw new Error("Fatal error");
  }
}

export async function getHighUrgency() {
  try {
    return "576";
  } catch (error) {
    console.error(error);
    throw new Error("Fatal error");
  }
}

export async function getMostReportedAreas() {
  try {
    return "56";
  } catch (error) {
    console.error(error);
    throw new Error("Fatal error");
  }
}

export async function getMostFrequentCategory() {
  try {
    return "38";
  } catch (error) {
    console.error(error);
    throw new Error("Fatal error");
  }
}
