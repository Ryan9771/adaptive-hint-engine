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
  } else {
    console.log("Failed to fetch entry");
  }

  return exerciseDetails;
}

export { post, getExerciseDetails };
