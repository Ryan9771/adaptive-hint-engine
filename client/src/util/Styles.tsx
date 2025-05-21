interface RawStyle {
  [key: string]: string[];
}

/* Concats a list of tailwind classes into a line */
export default function style(styles: RawStyle, style: string): string {
  return styles[style].join(" ") + " ";
}
