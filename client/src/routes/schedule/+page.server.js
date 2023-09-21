import {API_URL} from "$env/static/private";
import {error} from "@sveltejs/kit";

export const load = async ({ url }) => {
    const queryParams = getQueryParams(url);
    return await fetchSchedule(queryParams);
}


const fetchSchedule = async (scheduleData) => {

    let response;

    try {

        response = await fetch(
            `${API_URL}/api/v1/shifter/schedule/`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(scheduleData)
            }
        );

    } catch (err) { throw error(500, "Server could not be reached"); }


    const data = await response.json();
    if (response.ok) return data;
    else {
        throw error(500, data.detail.msg || data.detail);
    }

}

const getQueryParams = (url) => {

    const course_name = url.searchParams.get('course');
    const course_semester = url.searchParams.get('sem');
    const course_years = url.searchParams.get('year');

    return {
        course_name,
        course_semester,
        course_years
    }
}