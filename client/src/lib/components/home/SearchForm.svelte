<script>
    import {goto} from "$app/navigation";

    import {createCombobox, createRadioGroup} from "@melt-ui/svelte";
    import {Diamonds, DoubleBounce} from "svelte-loading-spinners";
    import {Search} from 'lucide-svelte';

    import {normalizeSemester, normalizeYear} from "$lib/utils/normalizers.js";
    import SemesterInput from "$lib/components/home/SemesterInput.svelte";
    import FormInput from "$lib/components/home/FormInput.svelte";
    import {navigating} from "$app/stores";

    export let courses = [
        "Licenciatura em Engenharia Informática",
        "Mestrado em Engenharia Informática",
        "Licenciatura em Direito"
    ];
    export let semesterOptions = ['Semester 1', 'Semester 2'];
    export let yearOptions = ['All', 'Year 1', 'Year 2', 'Year 3', 'Year 4']

    const courseSearchInput = createCombobox({forceVisible: true});
    const semesterRadioGroup = createRadioGroup({defaultValue: 'default', orientation: "horizontal"});
    const yearsCombobox = createCombobox({forceVisible: true});

    let isLoading = false;

    const submit = () => {

        isLoading = true;

        const queryParams = new URLSearchParams();

        const destroyCourseName = courseSearchInput.states.inputValue.subscribe((value) => {
            queryParams.set('course', value);
        });
        destroyCourseName();

        const destroySemester = semesterRadioGroup.states.value.subscribe((value) => {
            queryParams.set('sem', normalizeSemester(value));

        });
        destroySemester();

        const destroyYear = yearsCombobox.states.inputValue.subscribe((value) => {
            queryParams.set('year', normalizeYear(value));

        });
        destroyYear();

        goto("/schedule?" + queryParams.toString());
    }

</script>

<!-- lg: ultimos 2 | xl: ultimo | md: ultimos 3 | -->
<div class="flex flex-col p-10 bg-[#F7B155] rounded-md gap-3 sm:container md:w-1/2 lg:w-1/3">

    <!--<CourseNameInput {courses} {courseSearchInput}/>-->
    <FormInput builders={courseSearchInput} options={
        {
            values: courses,
            placeholder: "Select a course to continue",
            label: "Select a course:",
            styles: "w-full"
        }}
    />

    <div class="flex flex-row">

        <SemesterInput {semesterOptions} {semesterRadioGroup}/>

        <div class="ml-auto">

            <!--<CourseNameInput courses={yearOptions} courseSearchInput={yearsCombobox}/>-->
            <FormInput builders={yearsCombobox} options={
                {
                    values: yearOptions,
                    placeholder: "Year",
                    label: "",
                    styles: "w-1/2 ml-auto"
                }}
            />

        </div>

    </div>


    <button on:click={submit} class="h-10 rounded-md bg-magnum-600 px-3 py-1 text-magnum-100 hover:opacity-75 active:opacity-50">
        <span class="flex flex-row gap-2 justify-center items-center">
            {#if !$navigating}
                <Diamonds size="60" color="#fff9ed" unit="px"/>
            {:else}
                <span class="text-lg tracking-wide">SEARCH SCHEDULE</span>
            {/if}
        </span>
    </button>

    {#if !$navigating}


    {/if}

</div>