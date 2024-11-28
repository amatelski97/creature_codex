import { type MRT_HeaderGroup, type MRT_TableInstance, type MRT_VirtualItem } from '../types';
interface Props<TData extends Record<string, any> = {}> {
    footerGroup: MRT_HeaderGroup<TData>;
    table: MRT_TableInstance<TData>;
    virtualColumns?: MRT_VirtualItem[];
    virtualPaddingLeft?: number;
    virtualPaddingRight?: number;
}
export declare const MRT_TableFooterRow: <TData extends Record<string, any> = {}>({ footerGroup, table, virtualColumns, virtualPaddingLeft, virtualPaddingRight, }: Props<TData>) => import("react/jsx-runtime").JSX.Element | null;
export {};
