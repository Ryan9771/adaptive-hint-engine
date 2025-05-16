async function post(url = "", data = {}, token = "") {
  const response = await fetch(`http://localhost:5001${url}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(data),
  });

  return response;
}

async function getExerciseDetails(exerciseId: string) {
  const response = await post(`/exercise/${exerciseId}`);

  const exerciseDetails = {
    exerciseExists: false,
    exerciseTitle: "",
    exerciseDescription: "",
    exerciseText: "",
    skelCode: "",
    previousCode: "",
  };

  console.log("Response: ", response);

  if (response.ok) {
    const data = await response.json();
    /*
    Received Response format:
    {
      "exercise_title": string
      "exercise_text": string
      "skel_code": string
      "exercise_background": string
    }
    */
    exerciseDetails.exerciseExists = true;
    exerciseDetails.exerciseTitle = data.exercise_title;
    exerciseDetails.exerciseDescription = data.exercise_background;
    exerciseDetails.exerciseText = data.exercise_text;
    exerciseDetails.skelCode = data.skel_code;
    exerciseDetails.previousCode = data.previous_code;
  } else {
    console.log("Failed to fetch entry");
  }

  return exerciseDetails;
}

async function resetPreviousCode(exerciseId: string, skelCode: string) {
  const response = await post(`/exercise/reset/${exerciseId}`, {
    skel_code: skelCode,
  });

  if (response.ok) {
    console.log("Previous code reset successfully");
  } else {
    console.log("Failed to reset previous code");
  }
}

export { post, getExerciseDetails, resetPreviousCode };
