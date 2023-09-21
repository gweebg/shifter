<script>

    import {melt} from "@melt-ui/svelte";
    import {Check, ChevronDown, ChevronUp} from "lucide-svelte";
    import {fly} from 'svelte/transition';

    export let builders;
    export let options;

    const {
        elements: {menu, input, option, label},
        states: {open, inputValue, touchedInput},
        helpers: {isSelected},
    } = builders;

    $: filteredValues = $touchedInput
        ? options.values.filter((value) => {
            const normalizedInput = $inputValue.toLowerCase();
            return (
                value.toLowerCase().includes(normalizedInput)
            );
        })
        : options.values;

</script>

<div class="flex flex-col gap-1 it">

    <!-- Input Label -->
    <!-- svelte-ignore a11y-label-has-associated-control - $label contains the 'for' attribute -->
    <label use:melt={$label}>
        <span class="text-sm font-medium text-magnum-900">
            {options.label}
        </span>
    </label>

    <!-- Input element itself. -->
    <div class="relative">
        <input
            use:melt={$input}
            class="flex h-10 items-center justify-between rounded-lg bg-white px-3 pr-12 text-black {options.styles}"
            placeholder={options.placeholder}
        />

        <div class="absolute right-2 top-1/2 z-10 -translate-y-1/2 text-magnum-900">
            {#if $open}
                <ChevronUp class="square-4"/>
            {:else}
                <ChevronDown class="square-4"/>
            {/if}
        </div>
    </div>

</div>

{#if $open}
    <ul
        class="z-10 flex max-h-[300px] flex-col overflow-hidden rounded-lg"
        use:melt={$menu}
        transition:fly={{ duration: 150, y: -5 }}
    >
        <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
        <div
            class="flex max-h-full flex-col gap-0 overflow-y-auto bg-white px-2 py-2 text-black"
            tabindex="0"
        >
            {#each filteredValues as value}
                <li
                    use:melt={$option({
                            value: value,
                        })}
                    class="relative cursor-pointer scroll-my-2 rounded-md py-2 pl-4 pr-4
                               data-[highlighted]:bg-magnum-200 data-[highlighted]:text-magnum-900
                               data-[disabled]:opacity-50"
                >
                    {#if $isSelected(value)}
                        <div class="check absolute left-2 top-1/3 z-10 text-magnum-900">
                            <Check class="square-4"/>
                        </div>
                    {/if}
                    <div class="pl-4">
                        <span class="font-medium">{value}</span>
                    </div>
                </li>
            {:else}
                <li class="relative cursor-pointer rounded-md py-1 pl-8 pr-4 data-[highlighted]:bg-magnum-100 data-[highlighted]:text-magnum-700">
                    No results found
                </li>
            {/each}
        </div>
    </ul>
{/if}