import { type MRT_TableOptions, type MRT_TableInstance, type Xor } from './types';
type TableInstanceProp<TData extends Record<string, any> = {}> = {
    table: MRT_TableInstance<TData>;
};
type Props<TData extends Record<string, any> = {}> = Xor<TableInstanceProp<TData>, MRT_TableOptions<TData>>;
export declare const MantineReactTable: <TData extends Record<string, any> = {}>(props: Props<TData>) => import("react/jsx-runtime").JSX.Element;
export {};
