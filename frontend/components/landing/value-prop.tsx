import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function ValuePropositionSection() {
  const features = [
    {
      title: "Premium Aesthetics",
      description: "Experience a beautifully designed interface that makes task management enjoyable."
    },
    {
      title: "Intuitive Workflow",
      description: "Streamlined processes that boost productivity without adding complexity."
    },
    {
      title: "Advanced Security",
      description: "Enterprise-grade protection for your personal and professional data."
    }
  ];

  return (
    <section className="py-16">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12">Why Choose Our Solution</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card key={index} className="bg-card border-border">
              <CardHeader>
                <CardTitle>{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}