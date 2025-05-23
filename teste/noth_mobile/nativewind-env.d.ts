// nativewind-env.d.ts
declare module 'nativewind' {
  import type { TailwindCSS } from 'tailwindcss/types/config';
  const tw: TailwindCSS;
  export default tw;
}
