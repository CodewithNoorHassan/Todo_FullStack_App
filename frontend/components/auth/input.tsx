import { Input as BaseInput } from '@/components/ui/input';
import { cn } from '@/lib/utils';

interface AuthInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  required?: boolean;
}

export function AuthInput({ label, error, required, className, ...props }: AuthInputProps) {
  return (
    <div className="w-full">
      <label htmlFor={props.id} className="text-sm font-medium mb-1 block">
        {label} {required && <span className="text-destructive">*</span>}
      </label>
      <BaseInput
        {...props}
        className={cn(error ? 'border-destructive' : '', className)}
      />
      {error && <p className="text-destructive text-sm mt-1">{error}</p>}
    </div>
  );
}