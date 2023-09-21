<script>

    import {melt} from "@melt-ui/svelte";

    export let semesterOptions;
    export let semesterRadioGroup;

    const {
        elements: { root, item, hiddenInput },
        helpers: { isChecked },
    } = semesterRadioGroup;

</script>


<div
        use:melt={$root}
        class="flex gap-3 md:flex-row sm:flex-col flex-row"
        aria-label="View density"
>
    {#each semesterOptions as option}
        <div class="flex items-center gap-3">
            <button
                    use:melt={$item(option)}
                    class="grid h-5 w-5 cursor-pointer place-items-center rounded-full bg-white shadow-sm hover:bg-magnum-100"
                    id={option}
                    aria-labelledby="{option}-label"
            >
                {#if $isChecked(option)}
                    <div class="h-3 w-3 rounded-full bg-magnum-500" />
                {/if}
            </button>
            <label
                    class="font-medium capitalize leading-none text-magnum-900"
                    for={option}
                    id="{option}-label"
            >
                {option}
            </label>
        </div>
    {/each}
    <input name="line-height" use:melt={$hiddenInput} />
</div>