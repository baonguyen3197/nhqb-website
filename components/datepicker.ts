import { Datepicker } from 'flowbite';
import type { DatepickerOptions, DatepickerInterface } from 'flowbite';
import type { InstanceOptions } from 'flowbite';

// Set the target element of the input field or div
const $inlineDatepickerEl: HTMLElement = document.getElementById('datepicker-inline') as HTMLElement;

// Optional options with default values and callback functions
const options: DatepickerOptions = {
    defaultDatepickerId: null,
    autohide: false,
    format: 'mm/dd/yyyy',
    maxDate: null,
    minDate: null,
    orientation: 'bottom',
    buttons: false,
    autoSelectToday: 1, // Ensure this is a number
    title: null,
    rangePicker: false,
    onShow: () => {},
    onHide: () => {},
};

// Instance options object
const instanceOptions: InstanceOptions = {
  id: 'datepicker-inline-example',
  override: true
};

/*
 * $inlineDatepickerEl: required
 * options: optional
 * instanceOptions: optional
 */
const datepicker: DatepickerInterface = new Datepicker(
    $inlineDatepickerEl,
    options,
    instanceOptions
);

// Set today's date
const today = new Date();
const formattedDate = today.toLocaleDateString('en-US', {
    month: '2-digit',
    day: '2-digit',
    year: 'numeric'
});

// Use the underlying instance to set the date if setDate is not available
const datepickerInstance = (datepicker as any)._datepicker;
datepickerInstance.setDate(formattedDate);

// Disable pointer events to make the datepicker non-interactive
$inlineDatepickerEl.style.pointerEvents = 'none';