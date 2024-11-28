import { type MRT_TableInstance } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    isTopToolbar: boolean;
    table: MRT_TableInstance<TData>;
}
export declare const MRT_ProgressBar: <TData extends Record<string, any> = {}>({ isTopToolbar, table, }: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
