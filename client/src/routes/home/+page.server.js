import { API_URL } from '$env/static/private';
import { error } from "@sveltejs/kit";

export const load = async () => {

    let response;
    try {
        response = await fetch(`${API_URL}/api/v1/shifter/courses`);
    } catch (err) { throw error(500, "Api Server could not be reached, is the server running ?"); }

    if (response.ok) response = await response.json();
    else throw error(500, "Unexpected response from the server to /api/v1/courses");

    return {
        courses: response
    }

}


